import { useCallback, useEffect, useState } from "react";
import { api } from "../api/client";
import { useAuth } from "../context/AuthContext";
import Navbar from "../components/Navbar";
import SearchBar, { EMPTY_FILTERS } from "../components/SearchBar";
import VehicleCard from "../components/VehicleCard";
import VehicleFormModal from "../components/VehicleFormModal";

export default function DashboardPage() {
  const { token, isAdmin, logout } = useAuth();

  const [vehicles, setVehicles] = useState([]);
  const [filters, setFilters] = useState(EMPTY_FILTERS);
  const [loading, setLoading] = useState(true);
  const [notice, setNotice] = useState(null); // { type: "success" | "error", text }
  const [editing, setEditing] = useState(null); // null = closed, {} = new, vehicle = edit

  const showNotice = (type, text) => {
    setNotice({ type, text });
    setTimeout(() => setNotice(null), 3000);
  };

  // Wraps every API action: shows errors, and logs out if the token expired.
  const run = useCallback(async (action, successText) => {
    try {
      await action();
      if (successText) showNotice("success", successText);
      return true;
    } catch (err) {
      if (err.status === 401) logout();
      else showNotice("error", err.message);
      return false;
    }
  }, [logout]);

  const loadVehicles = useCallback(async (activeFilters = filters) => {
    const hasFilters = Object.values(activeFilters).some((value) => value !== "");
    await run(async () => {
      const result = hasFilters ? await api.searchVehicles(token, activeFilters) : await api.listVehicles(token);
      setVehicles(result);
    });
    setLoading(false);
  }, [filters, run, token]);

  useEffect(() => {
    loadVehicles(EMPTY_FILTERS);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  function handleSearch(newFilters) {
    setFilters(newFilters);
    loadVehicles(newFilters);
  }

  // Swap one updated vehicle into the list without refetching everything.
  const replaceVehicle = (updated) => setVehicles((list) => list.map((v) => (v.id === updated.id ? updated : v)));

  const handlePurchase = (vehicle) =>
    run(async () => replaceVehicle(await api.purchaseVehicle(token, vehicle.id)),
      `You bought a ${vehicle.make} ${vehicle.model}!`);

  const handleRestock = (vehicle) => {
    const amount = Number(prompt(`How many ${vehicle.model} units to add?`, "5"));
    if (!amount) return;
    run(async () => replaceVehicle(await api.restockVehicle(token, vehicle.id, amount)), "Stock updated");
  };

  const handleDelete = (vehicle) => {
    if (!confirm(`Delete ${vehicle.make} ${vehicle.model}?`)) return;
    run(async () => {
      await api.deleteVehicle(token, vehicle.id);
      setVehicles((list) => list.filter((v) => v.id !== vehicle.id));
    }, "Vehicle deleted");
  };

  async function handleSave(data) {
    // Errors here are thrown on purpose so the modal can show them inline.
    if (editing.id) {
      replaceVehicle(await api.updateVehicle(token, editing.id, data));
    } else {
      await api.addVehicle(token, data);
      await loadVehicles();
    }
    setEditing(null);
    showNotice("success", "Vehicle saved");
  }

  return (
    <>
      <Navbar />
      <main className="mx-auto max-w-6xl px-4 py-8">
        <div className="mb-6 flex flex-wrap items-end justify-between gap-4">
          <div>
            <h1 className="font-display text-4xl font-bold tracking-tight">Showroom</h1>
            <p className="text-sm text-stone-400">{vehicles.length} vehicles</p>
          </div>
          {isAdmin && <button className="btn-primary" onClick={() => setEditing({})}>+ Add vehicle</button>}
        </div>

        <SearchBar onSearch={handleSearch} />

        {loading ? (
          <p className="mt-10 text-center text-stone-400">Loading…</p>
        ) : vehicles.length === 0 ? (
          <p className="mt-10 text-center text-stone-400">No vehicles found.</p>
        ) : (
          <section className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {vehicles.map((vehicle) => (
              <VehicleCard
                key={vehicle.id}
                vehicle={vehicle}
                isAdmin={isAdmin}
                onPurchase={handlePurchase}
                onEdit={setEditing}
                onDelete={handleDelete}
                onRestock={handleRestock}
              />
            ))}
          </section>
        )}
      </main>

      {editing && (
        <VehicleFormModal vehicle={editing.id ? editing : null} onSave={handleSave} onClose={() => setEditing(null)} />
      )}

      {notice && (
        <div
          role="status"
          className={`fixed bottom-6 right-6 rounded-lg px-4 py-3 text-sm font-medium shadow-lg ${
            notice.type === "success" ? "bg-emerald-500 text-stone-950" : "bg-red-500 text-white"
          }`}
        >
          {notice.text}
        </div>
      )}
    </>
  );
}