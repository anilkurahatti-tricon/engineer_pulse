// Data-service layer for the Employee Skills controller.
import apiClient from "./apiClient";

const BASE_PATH = "/api/employee-skills/";

export const employeeSkillsDataService = {
  getAll: () => apiClient.get(BASE_PATH).then((res) => res.data),
  getById: (id) => apiClient.get(`${BASE_PATH}${id}`).then((res) => res.data),
  create: (payload) => apiClient.post(BASE_PATH, payload).then((res) => res.data),
  update: (id, payload) => apiClient.put(`${BASE_PATH}${id}`, payload).then((res) => res.data),
  remove: (id) => apiClient.delete(`${BASE_PATH}${id}`),
};
