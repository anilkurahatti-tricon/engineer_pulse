// Data-service layer for the Chatbot controller.
import apiClient from "./apiClient";

const BASE_PATH = "/api/chatbot/";

export const chatbotDataService = {
  getAll: () => apiClient.get(BASE_PATH).then((res) => res.data),
  ask: (sessionId, message) =>
    apiClient.post(`${BASE_PATH}ask`, { session_id: sessionId, message }).then((res) => res.data),
};
