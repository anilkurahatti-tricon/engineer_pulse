// Business layer: React hook wrapping the Chatbot data-service.
import { useCallback, useState } from "react";
import { chatbotDataService } from "../dataservice/chatbotDataService";

const DEFAULT_SESSION_ID = "session-ui";

export function useChatbot() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const sendMessage = useCallback(async (text) => {
    setLoading(true);
    setError(null);
    setMessages((prev) => [...prev, { sender: "user", message: text }]);
    try {
      const response = await chatbotDataService.ask(DEFAULT_SESSION_ID, text);
      setMessages((prev) => [...prev, { sender: "bot", message: response.reply }]);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  return { messages, loading, error, sendMessage };
}
