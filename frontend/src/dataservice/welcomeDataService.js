// Data-service layer for the Welcome controller.
import apiClient from "./apiClient";

const BASE_PATH = "/api/welcome/";

export const welcomeDataService = {
  get: () => apiClient.get(BASE_PATH).then((res) => res.data),
};
