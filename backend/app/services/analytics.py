from datetime import datetime
from typing import Dict, List

from app.db.databricks_client import DatabricksClient


MOCK_DATA = [
    {"state": "Maharashtra", "month": "2025-01", "accidents": 3200},
    {"state": "Karnataka", "month": "2025-01", "accidents": 2750},
    {"state": "Tamil Nadu", "month": "2025-01", "accidents": 2600},
    {"state": "Uttar Pradesh", "month": "2025-01", "accidents": 3000},
    {"state": "Rajasthan", "month": "2025-01", "accidents": 1800},
    {"state": "Maharashtra", "month": "2025-02", "accidents": 3400},
    {"state": "Karnataka", "month": "2025-02", "accidents": 2810},
    {"state": "Tamil Nadu", "month": "2025-02", "accidents": 2550},
    {"state": "Uttar Pradesh", "month": "2025-02", "accidents": 3150},
    {"state": "Rajasthan", "month": "2025-02", "accidents": 1900},
]


class AnalyticsService:
    def __init__(self) -> None:
        self.client = DatabricksClient()

    def _query_or_mock(self, query: str) -> List[Dict]:
        try:
            return self.client.execute_query(query)
        except Exception:
            return []

    def _build_from_mock(self) -> Dict:
        totals: Dict[str, int] = {}
        trend: Dict[str, int] = {}
        for row in MOCK_DATA:
            totals[row["state"]] = totals.get(row["state"], 0) + int(row["accidents"])
            trend[row["month"]] = trend.get(row["month"], 0) + int(row["accidents"])

        totals_by_state = [{"state": k, "accidents": v} for k, v in totals.items()]
        totals_by_state.sort(key=lambda x: x["accidents"], reverse=True)
        trend_data = [{"month": k, "accidents": v} for k, v in sorted(trend.items())]

        return {
            "totals_by_state": totals_by_state,
            "top_5_dangerous_states": totals_by_state[:5],
            "trend": trend_data,
            "total_accidents": sum(totals.values()),
        }

    def get_stats(self) -> Dict:
        # Expected schema in Delta table `accidents`:
        # state STRING, month STRING (YYYY-MM), accidents INT
        totals_query = """
            SELECT state, SUM(accidents) AS accidents
            FROM accidents
            GROUP BY state
            ORDER BY accidents DESC
        """
        trend_query = """
            SELECT month, SUM(accidents) AS accidents
            FROM accidents
            GROUP BY month
            ORDER BY month
        """

        totals = self._query_or_mock(totals_query)
        trend = self._query_or_mock(trend_query)

        if not totals or not trend:
            return self._build_from_mock()

        normalized_totals = [
            {"state": row["state"], "accidents": int(row["accidents"])} for row in totals
        ]
        normalized_trend = [
            {"month": row["month"], "accidents": int(row["accidents"])} for row in trend
        ]

        return {
            "totals_by_state": normalized_totals,
            "top_5_dangerous_states": normalized_totals[:5],
            "trend": normalized_trend,
            "total_accidents": sum(item["accidents"] for item in normalized_totals),
        }

    def predict_risk(self) -> Dict:
        stats = self.get_stats()
        max_acc = max((item["accidents"] for item in stats["totals_by_state"]), default=1)

        risk_map = []
        for item in stats["totals_by_state"]:
            ratio = item["accidents"] / max_acc
            if ratio >= 0.75:
                risk = "high"
            elif ratio >= 0.45:
                risk = "medium"
            else:
                risk = "low"
            risk_map.append({"state": item["state"], "risk": risk})

        return {"risk_map": risk_map, "generated_at": datetime.utcnow().isoformat()}
