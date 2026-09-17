import { useState } from "react";
import { useDemoItems } from "../business/useDemoItems";

export default function DemoPage() {
  const { items, loading, error, createItem, deleteItem } = useDemoItems();
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!name || !description) return;
    await createItem({ name, description });
    setName("");
    setDescription("");
  };

  return (
    <section>
      <h1>Demo (CRUD sanity check)</h1>
      <form onSubmit={handleSubmit} className="form-row">
        <input placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} />
        <input
          placeholder="Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
        <button type="submit">Add</button>
      </form>

      {loading && <p>Loading...</p>}
      {error && <p className="error">{error}</p>}

      <ul className="item-list">
        {items.map((item) => (
          <li key={item.id}>
            <strong>{item.name}</strong> - {item.description}
            <button onClick={() => deleteItem(item.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </section>
  );
}
