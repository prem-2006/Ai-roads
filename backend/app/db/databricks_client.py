from contextlib import contextmanager
from typing import Any, Dict, List

from databricks import sql

from app.config import get_settings


class DatabricksClient:
    def __init__(self) -> None:
        self.settings = get_settings()

    @contextmanager
    def _connect(self):
        connection = sql.connect(
            server_hostname=self.settings.databricks_server_hostname,
            http_path=self.settings.databricks_http_path,
            access_token=self.settings.databricks_access_token,
        )
        try:
            yield connection
        finally:
            connection.close()

    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        with self._connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                columns = [c[0] for c in cursor.description]
                rows = cursor.fetchall()
                return [dict(zip(columns, row)) for row in rows]
