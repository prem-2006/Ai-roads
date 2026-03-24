import { useEffect, useMemo, useState } from "react";
import { ComposableMap, Geographies, Geography } from "react-simple-maps";
import { getRiskPrediction } from "../api/client";
import LoadingSpinner from "../components/LoadingSpinner";
import ErrorBanner from "../components/ErrorBanner";

const INDIA_GEOJSON =
  "https://raw.githubusercontent.com/geohacker/india/master/state/india_telengana.geojson";

const riskColor = {
  high: "#ef4444",
  medium: "#facc15",
  low: "#22c55e",
};

export default function HeatmapPage() {
  const [riskData, setRiskData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    (async () => {
      try {
        setLoading(true);
        const response = await getRiskPrediction();
        setRiskData(response.risk_map || []);
      } catch (err) {
        setError(err?.response?.data?.detail || err.message || "Failed to load heatmap data.");
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const riskLookup = useMemo(() => {
    const map = {};
    for (const item of riskData) map[item.state?.toLowerCase()] = item.risk;
    return map;
  }, [riskData]);

  if (loading) return <LoadingSpinner text="Generating risk heatmap..." />;

  return (
    <section className="glass heatmap-card">
      <h2>India High-Risk States Heatmap</h2>
      <ErrorBanner message={error} />
      <div className="legend">
        <span><i style={{ background: riskColor.high }} /> High</span>
        <span><i style={{ background: riskColor.medium }} /> Medium</span>
        <span><i style={{ background: riskColor.low }} /> Low</span>
      </div>
      <ComposableMap projection="geoMercator" projectionConfig={{ scale: 850, center: [82, 22] }}>
        <Geographies geography={INDIA_GEOJSON}>
          {({ geographies }) =>
            geographies.map((geo) => {
              const stateName = String(geo.properties.NAME_1 || geo.properties.st_nm || "").toLowerCase();
              const risk = riskLookup[stateName] || "low";
              return (
                <Geography
                  key={geo.rsmKey}
                  geography={geo}
                  fill={riskColor[risk]}
                  stroke="#0f172a"
                  style={{
                    default: { outline: "none" },
                    hover: { fill: "#ffffff", outline: "none" },
                    pressed: { outline: "none" },
                  }}
                />
              );
            })
          }
        </Geographies>
      </ComposableMap>
    </section>
  );
}
