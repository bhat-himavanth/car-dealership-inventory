import { useAuth } from "../context/AuthContext";

export default function Navbar() {
  const { user, isAdmin, logout } = useAuth();

  return (
    <header className="sticky top-0 z-10 border-b border-stone-800 bg-stone-950/80 backdrop-blur">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
        <span className="font-display text-xl font-bold">
          Auto<span className="text-amber-400">Vault</span>
        </span>
        <div className="flex items-center gap-3 text-sm">
          <span className="hidden text-stone-400 sm:inline">{user?.email}</span>
          {isAdmin && (
            <span className="rounded-full bg-amber-400/15 px-2 py-0.5 text-xs font-semibold text-amber-300">ADMIN</span>
          )}
          <button onClick={logout} className="btn-ghost">Log out</button>
        </div>
      </div>
    </header>
  );
}