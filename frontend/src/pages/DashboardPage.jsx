import { useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  CartesianGrid,
  Tooltip,
  XAxis,
  YAxis,
  ResponsiveContainer,
  LineChart,
  Line,
} from "recharts";
import { getStats } from "../api/client";
import LoadingSpinner from "../components/LoadingSpinner";
import ErrorBanner from "../components/ErrorBanner";

export default function DashboardPage() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    (async () => {
      try {
        setLoading(true);
        const response = await getStats();
        setStats(response);
      } catch (err) {
        setError(err?.response?.data?.detail || err.message || "Failed to load dashboard data.");
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  if (loading) return <LoadingSpinner text="Fetching accident analytics..." />;

  return (
    <section className="page-grid">
      <ErrorBanner message={error} />

      <article className="glass card">
        <h2>Total Accidents</h2>
        <p className="metric">{stats?.total_accidents ?? 0}</p>
      </article>

      <article className="glass card">
        <h2>Top 5 Dangerous States</h2>
        <ul className="top-list">
          {(stats?.top_5_dangerous_states || []).map((state) => (
            <li key={state.state}>
              <span>{state.state}</span>
              <strong>{state.accidents}</strong>
            </li>
          ))}
        </ul>
      </article>

      <article className="glass chart-card">
        <h2>Accidents by State</h2>
        <div className="chart-wrap">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={stats?.totals_by_state || []}>
              <CartesianGrid strokeDasharray="3 3" stroke="#2b3952" />
              <XAxis dataKey="state" stroke="#b3c4de" />
              <YAxis stroke="#b3c4de" />
              <Tooltip />
              <Bar dataKey="accidents" fill="#7c5cff" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </article>

      <article className="glass chart-card">
        <h2>Accident Trend</h2>
        <div className="chart-wrap">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={stats?.trend || []}>
              <CartesianGrid strokeDasharray="3 3" stroke="#2b3952" />
              <XAxis dataKey="month" stroke="#b3c4de" />
              <YAxis stroke="#b3c4de" />
              <Tooltip />
              <Line type="monotone" dataKey="accidents" stroke="#3ee9c7" strokeWidth={3} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </article>
    </section>
  );
}
