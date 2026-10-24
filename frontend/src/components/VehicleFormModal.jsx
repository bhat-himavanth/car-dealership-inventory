// One form for both "Add vehicle" and "Edit vehicle".
// If a vehicle is passed in, the form starts filled with its details.
import { useState } from "react";

const BLANK = { make: "", model: "", category: "", price: "", quantity: "" };

export default function VehicleFormModal({ vehicle, onSave, onClose }) {
  const [form, setForm] = useState(vehicle ?? BLANK);
  const [error, setError] = useState("");

  const update = (field) => (event) => setForm({ ...form, [field]: event.target.value });

  async function handleSubmit(event) {
    event.preventDefault();
    try {
      await onSave({
        make: form.make,
        model: form.model,
        category: form.category,
        price: Number(form.price),
        quantity: Number(form.quantity),
      });
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div className="fixed inset-0 z-20 grid place-items-center bg-black/70 px-4" onClick={onClose}>
      <form
        onSubmit={handleSubmit}
        onClick={(e) => e.stopPropagation()}
        className="w-full max-w-md space-y-3 rounded-2xl border border-stone-700 bg-stone-900 p-6"
      >
        <h2 className="font-display text-2xl font-bold">{vehicle ? "Edit vehicle" : "Add vehicle"}</h2>

        <input className="input" placeholder="Make" required value={form.make} onChange={update("make")} />
        <input className="input" placeholder="Model" required value={form.model} onChange={update("model")} />
        <input className="input" placeholder="Category" required value={form.category} onChange={update("category")} />
        <div className="grid grid-cols-2 gap-3">
          <input className="input" type="number" min="1" placeholder="Price" required value={form.price} onChange={update("price")} />
          <input className="input" type="number" min="0" placeholder="Quantity" required value={form.quantity} onChange={update("quantity")} />
        </div>

        {error && <p role="alert" className="text-sm text-red-400">{error}</p>}

        <div className="flex justify-end gap-2 pt-2">
          <button type="button" className="btn-ghost" onClick={onClose}>Cancel</button>
          <button className="btn-primary">Save</button>
        </div>
      </form>
    </div>
  );
}