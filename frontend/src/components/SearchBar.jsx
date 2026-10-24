import { useState } from "react";

export const EMPTY_FILTERS = { make: "", model: "", category: "", min_price: "", max_price: "" };

export default function SearchBar({ onSearch }) {
  const [filters, setFilters] = useState(EMPTY_FILTERS);

  const update = (field) => (event) => setFilters({ ...filters, [field]: event.target.value });

  function handleSubmit(event) {
    event.preventDefault();
    onSearch(filters);
  }

  function handleReset() {
    setFilters(EMPTY_FILTERS);
    onSearch(EMPTY_FILTERS);
  }

  return (
    <form onSubmit={handleSubmit} className="grid gap-3 rounded-2xl border border-stone-800 bg-stone-900/60 p-4 sm:grid-cols-2 lg:grid-cols-6">
      <input className="input" placeholder="Make" aria-label="Make" value={filters.make} onChange={update("make")} />
      <input className="input" placeholder="Model" aria-label="Model" value={filters.model} onChange={update("model")} />
      <input className="input" placeholder="Category (SUV, Sedan…)" aria-label="Category" value={filters.category} onChange={update("category")} />
      <input className="input" type="number" min="0" placeholder="Min price" aria-label="Min price" value={filters.min_price} onChange={update("min_price")} />
      <input className="input" type="number" min="0" placeholder="Max price" aria-label="Max price" value={filters.max_price} onChange={update("max_price")} />
      <div className="flex gap-2">
        <button className="btn-primary flex-1">Search</button>
        <button type="button" onClick={handleReset} className="btn-ghost">Clear</button>
      </div>
    </form>
  );
}