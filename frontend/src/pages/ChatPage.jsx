import { useState } from "react";
import { askAssistant } from "../api/client";
import LoadingSpinner from "../components/LoadingSpinner";
import ErrorBanner from "../components/ErrorBanner";

export default function ChatPage() {
  const [messages, setMessages] = useState([
    { role: "assistant", content: "Ask me anything about road accident trends and high-risk states." },
  ]);
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const onSubmit = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;

    const userMessage = { role: "user", content: question.trim() };
    setMessages((prev) => [...prev, userMessage]);
    setQuestion("");
    setError("");
    setLoading(true);

    try {
      const response = await askAssistant(userMessage.content);
      setMessages((prev) => [...prev, { role: "assistant", content: response.answer }]);
    } catch (err) {
      setError(err?.response?.data?.detail || err.message || "Assistant request failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="chat-shell glass">
      <h2>AI Road Safety Assistant</h2>
      <ErrorBanner message={error} />
      <div className="chat-window">
        {messages.map((msg, idx) => (
          <div key={`${msg.role}-${idx}`} className={`msg ${msg.role}`}>
            {msg.content}
          </div>
        ))}
        {loading && <LoadingSpinner text="Thinking..." />}
      </div>
      <form className="chat-input-row" onSubmit={onSubmit}>
        <input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder='Try: "Which state has highest accidents?"'
        />
        <button type="submit" disabled={loading}>
          Send
        </button>
      </form>
    </section>
  );
}
