import { useState } from "react";
import { useEmployeeFeedback } from "../business/useEmployeeFeedback";

export default function EmployeeFeedbackPage() {
  const { items, loading, error, createItem, deleteItem } = useEmployeeFeedback();
  const [employeeName, setEmployeeName] = useState("");
  const [feedbackText, setFeedbackText] = useState("");
  const [rating, setRating] = useState(5);

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!employeeName || !feedbackText) return;
    await createItem({
      employee_id: Math.floor(Math.random() * 1000),
      employee_name: employeeName,
      feedback_text: feedbackText,
      rating: Number(rating),
    });
    setEmployeeName("");
    setFeedbackText("");
    setRating(5);
  };

  return (
    <section>
      <h1>Employee Feedback</h1>
      <form onSubmit={handleSubmit} className="form-row">
        <input
          placeholder="Employee name"
          value={employeeName}
          onChange={(e) => setEmployeeName(e.target.value)}
        />
        <input
          placeholder="Feedback"
          value={feedbackText}
          onChange={(e) => setFeedbackText(e.target.value)}
        />
        <input
          type="number"
          min="1"
          max="5"
          value={rating}
          onChange={(e) => setRating(e.target.value)}
        />
        <button type="submit">Add</button>
      </form>

      {loading && <p>Loading...</p>}
      {error && <p className="error">{error}</p>}

      <ul className="item-list">
        {items.map((item) => (
          <li key={item.id}>
            <strong>{item.employee_name}</strong> ({item.rating}/5): {item.feedback_text}
            <button onClick={() => deleteItem(item.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </section>
  );
}
