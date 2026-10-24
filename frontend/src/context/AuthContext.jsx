// Holds "who is logged in" for the whole app, so any component can read it
// with useAuth() instead of passing the token down through every prop.
import { createContext, useContext, useState } from "react";
import { api } from "../api/client";

const AuthContext = createContext(null);
const STORAGE_KEY = "dealership-auth";

function loadSavedSession() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY));
  } catch {
    return null;
  }
}

export function AuthProvider({ children }) {
  // Saved in localStorage so a page refresh doesn't log you out.
  const [session, setSession] = useState(loadSavedSession);

  async function login(email, password) {
    const { access_token, user } = await api.login(email, password);
    const newSession = { token: access_token, user };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(newSession));
    setSession(newSession);
  }

  function logout() {
    localStorage.removeItem(STORAGE_KEY);
    setSession(null);
  }

  const value = {
    token: session?.token,
    user: session?.user,
    isAdmin: Boolean(session?.user?.is_admin),
    login,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  return useContext(AuthContext);
}