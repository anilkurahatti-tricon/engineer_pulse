// Placeholder landing page - swap the copy/design here whenever real content is ready.
import { Link } from "react-router-dom";
import { useWelcome } from "../business/useWelcome";

const FALLBACK_FEATURES = [
  { title: "Employee Feedback", description: "Capture and review feedback for every engineer.", path: "/employee-feedback" },
  { title: "Employee Skills", description: "Track skills and proficiency levels across the team.", path: "/employee-skills" },
  { title: "AI Chatbot", description: "Ask questions and get AI-assisted answers.", path: "/chatbot" },
  { title: "Demo Sandbox", description: "Full CRUD playground used to validate the layered setup.", path: "/demo" },
];

export default function WelcomePage() {
  const { info, loading, error } = useWelcome();
  const features = info?.features?.length ? info.features : FALLBACK_FEATURES;

  return (
    <section className="welcome">
      <div className="welcome-hero">
        <h1>{info?.app_name || "Engineer Pulse"}</h1>
        <p className="welcome-tagline">
          {info?.tagline || "Understand, support, and grow your engineering team."}
        </p>
        {error && <p className="error">Couldn&apos;t reach the API: {error}</p>}
        {loading && <p>Loading welcome details...</p>}
        {info?.description && <p className="welcome-description">{info.description}</p>}
      </div>

      <div className="welcome-grid">
        {features.map((feature) => (
          <Link to={feature.path} key={feature.title} className="welcome-card">
            <h2>{feature.title}</h2>
            <p>{feature.description}</p>
          </Link>
        ))}
      </div>
    </section>
  );
}
