// Axios instance shared by every data-service module. Base URL is read from
// the .env file (VITE_API_BASE_URL) so it can point at any backend without
// code changes.
import axios from "axios";

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

export default apiClient;
