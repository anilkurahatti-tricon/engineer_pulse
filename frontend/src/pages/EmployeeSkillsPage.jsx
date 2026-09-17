import { useState } from "react";
import { useEmployeeSkills } from "../business/useEmployeeSkills";

export default function EmployeeSkillsPage() {
  const { items, loading, error, createItem, deleteItem } = useEmployeeSkills();
  const [employeeName, setEmployeeName] = useState("");
  const [skillName, setSkillName] = useState("");
  const [proficiencyLevel, setProficiencyLevel] = useState("Beginner");

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!employeeName || !skillName) return;
    await createItem({
      employee_id: Math.floor(Math.random() * 1000),
      employee_name: employeeName,
      skill_name: skillName,
      proficiency_level: proficiencyLevel,
    });
    setEmployeeName("");
    setSkillName("");
    setProficiencyLevel("Beginner");
  };

  return (
    <section>
      <h1>Employee Skills</h1>
      <form onSubmit={handleSubmit} className="form-row">
        <input
          placeholder="Employee name"
          value={employeeName}
          onChange={(e) => setEmployeeName(e.target.value)}
        />
        <input placeholder="Skill" value={skillName} onChange={(e) => setSkillName(e.target.value)} />
        <select value={proficiencyLevel} onChange={(e) => setProficiencyLevel(e.target.value)}>
          <option>Beginner</option>
          <option>Intermediate</option>
          <option>Advanced</option>
        </select>
        <button type="submit">Add</button>
      </form>

      {loading && <p>Loading...</p>}
      {error && <p className="error">{error}</p>}

      <ul className="item-list">
        {items.map((item) => (
          <li key={item.id}>
            <strong>{item.employee_name}</strong> - {item.skill_name} ({item.proficiency_level})
            <button onClick={() => deleteItem(item.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </section>
  );
}
