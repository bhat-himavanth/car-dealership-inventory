const formatPrice = (price) =>
  new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR", maximumFractionDigits: 0 }).format(price);

export default function VehicleCard({ vehicle, isAdmin, onPurchase, onEdit, onDelete, onRestock }) {
  const outOfStock = vehicle.quantity === 0;

  return (
    <article className="flex flex-col rounded-2xl border border-stone-800 bg-stone-900/60 p-5 transition hover:border-stone-600">
      <div className="flex items-start justify-between gap-2">
        <div>
          <p className="text-xs uppercase tracking-widest text-stone-500">{vehicle.make}</p>
          <h3 className="font-display text-2xl font-bold">{vehicle.model}</h3>
        </div>
        <span className="rounded-full border border-stone-700 px-2 py-0.5 text-xs text-stone-300">{vehicle.category}</span>
      </div>

      <p className="mt-4 font-display text-xl text-amber-400">{formatPrice(vehicle.price)}</p>
      <p className={`mt-1 text-sm ${outOfStock ? "text-red-400" : "text-emerald-400"}`}>
        {outOfStock ? "Out of stock" : `${vehicle.quantity} in stock`}
      </p>

      <button className="btn-primary mt-5" disabled={outOfStock} onClick={() => onPurchase(vehicle)}>
        {outOfStock ? "Sold out" : "Purchase"}
      </button>

      {isAdmin && (
        <div className="mt-3 grid grid-cols-3 gap-2">
          <button className="btn-ghost" onClick={() => onEdit(vehicle)}>Edit</button>
          <button className="btn-ghost" onClick={() => onRestock(vehicle)}>Restock</button>
          <button className="btn-ghost hover:!border-red-500 hover:!text-red-400" onClick={() => onDelete(vehicle)}>
            Delete
          </button>
        </div>
      )}
    </article>
  );
}