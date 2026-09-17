import { NavLink } from "react-router-dom";

const linkClass = ({ isActive }) => (isActive ? "nav-link nav-link-active" : "nav-link");

export default function NavBar() {
  return (
    <nav className="navbar">
      <span className="navbar-brand">Engineer Pulse</span>
      <NavLink to="/" end className={linkClass}>
        Welcome
      </NavLink>
      <NavLink to="/demo" className={linkClass}>
        Demo
      </NavLink>
      <NavLink to="/employee-feedback" className={linkClass}>
        Employee Feedback
      </NavLink>
      <NavLink to="/employee-skills" className={linkClass}>
        Employee Skills
      </NavLink>
      <NavLink to="/chatbot" className={linkClass}>
        Chatbot
      </NavLink>
    </nav>
  );
}
