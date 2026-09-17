import { useState } from "react";
import { useChatbot } from "../business/useChatbot";

export default function ChatbotPage() {
  const { messages, loading, error, sendMessage } = useChatbot();
  const [text, setText] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!text) return;
    const toSend = text;
    setText("");
    await sendMessage(toSend);
  };

  return (
    <section>
      <h1>Chatbot</h1>
      <div className="chat-window">
        {messages.map((m, idx) => (
          <p key={idx} className={m.sender === "user" ? "chat-user" : "chat-bot"}>
            <strong>{m.sender === "user" ? "You" : "Bot"}:</strong> {m.message}
          </p>
        ))}
      </div>

      {loading && <p>Thinking...</p>}
      {error && <p className="error">{error}</p>}

      <form onSubmit={handleSubmit} className="form-row">
        <input
          placeholder="Ask the chatbot..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
        <button type="submit">Send</button>
      </form>
    </section>
  );
}
