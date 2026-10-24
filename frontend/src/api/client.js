// One place that knows how to talk to the backend.
// Components call these functions instead of using fetch() directly.

const BASE_URL = import.meta.env.VITE_API_URL ?? "";

async function request(path, { method = "GET", body, token } = {}) {
  const headers = { "Content-Type": "application/json" };
  if (token) headers.Authorization = `Bearer ${token}`;

  const response = await fetch(`${BASE_URL}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });

  if (response.status === 204) return null;

  const data = await response.json().catch(() => null);
  if (!response.ok) {
    // FastAPI puts error text in "detail" (a string, or a list for validation errors)
    const detail = data?.detail;
    const message = Array.isArray(detail) ? detail.map((d) => d.msg).join(", ") : detail;
    const error = new Error(message || "Something went wrong");
    error.status = response.status;
    throw error;
  }
  return data;
}

export const api = {
  register: (email, password) => request("/api/auth/register", { method: "POST", body: { email, password } }),
  login: (email, password) => request("/api/auth/login", { method: "POST", body: { email, password } }),

  listVehicles: (token) => request("/api/vehicles", { token }),
  searchVehicles: (token, filters) => {
    // Drop empty filters so we don't send "?make=&model="
    const params = new URLSearchParams(Object.entries(filters).filter(([, value]) => value !== ""));
    return request(`/api/vehicles/search?${params}`, { token });
  },
  addVehicle: (token, vehicle) => request("/api/vehicles", { method: "POST", body: vehicle, token }),
  updateVehicle: (token, id, changes) => request(`/api/vehicles/${id}`, { method: "PUT", body: changes, token }),
  deleteVehicle: (token, id) => request(`/api/vehicles/${id}`, { method: "DELETE", token }),
  purchaseVehicle: (token, id) => request(`/api/vehicles/${id}/purchase`, { method: "POST", token }),
  restockVehicle: (token, id, amount) =>
    request(`/api/vehicles/${id}/restock`, { method: "POST", body: { amount }, token }),
};