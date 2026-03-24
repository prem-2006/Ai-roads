import { NavLink } from "react-router-dom";

const links = [
  { to: "/", label: "Dashboard" },
  { to: "/heatmap", label: "Heatmap" },
  { to: "/assistant", label: "AI Assistant" },
];

export default function Navbar() {
  return (
    <header className="glass nav-shell">
      <h1>Road Accident Intelligence System</h1>
      <nav>
        {links.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            className={({ isActive }) => (isActive ? "nav-link active" : "nav-link")}
          >
            {link.label}
          </NavLink>
        ))}
      </nav>
    </header>
  );
}
