import axios from "axios";

// backend URL
const BASE_URL = "http://127.0.0.1:5000";

// Create axios instance 
const api = axios.create({
  baseURL: BASE_URL,
  headers: { "Content-Type": "application/json" }
});

// Auto-attach JWT token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle expired tokens
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("token");
      localStorage.removeItem("user");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

// AUTH 
export const authAPI = {
  register: (username, email, password) =>
    api.post("/api/register", { username, email, password }),

  login: (username, password) =>
    api.post("/api/login", { username, password }),

  getProfile: () =>
    api.get("/api/profile")
};

// OBJECTS 
export const objectsAPI = {
  upload: (formData) =>
    api.post("/api/objects/upload", formData, {
      headers: { "Content-Type": "multipart/form-data" }
    }),

  list: (sort = "date") =>
    api.get(`/api/objects/list?sort=${sort}`),

  download: (filename) =>
    api.get(`/api/objects/download/${filename}`, { responseType: "blob" }),

  delete: (filename) =>
    api.delete(`/api/objects/${filename}`),

  storageInfo: () =>
    api.get("/api/objects/storage")
};

// USAGE 
export const usageAPI = {
  today: ()              => api.get("/api/usage/today"),
  history: (days = 30)   => api.get(`/api/usage/history?days=${days}`),
  currentMonth: ()       => api.get("/api/usage/current-month"),
  monthly: (year, month) => api.get(`/api/usage/monthly?year=${year}&month=${month}`),
  alltime: ()            => api.get("/api/usage/alltime")
};

// BILLING 
export const billingAPI = {
  estimate: ()                    => api.get("/api/billing/estimate"),
  calculate: (year, month)        => api.get(`/api/billing/calculate?year=${year}&month=${month}`),
  generate: (year, month)         => api.post("/api/billing/generate", { year, month }),
  listInvoices: ()                => api.get("/api/billing/invoices"),
  getInvoice: (id)                => api.get(`/api/billing/invoices/${id}`),
  payInvoice: (id)                => api.post(`/api/billing/invoices/${id}/pay`)
};

export default api;