from typing import Optional

import requests

from tracesql.model import ApiResponse, DbModel


class TraceSQLClient:
    BASE_URL = "https://tracesql.com/api/analyze"

    def __init__(self, api_key: Optional[str] = None):
        self.headers = {
            "Content-Type": "application/json",
        }
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"

    def analyze_lineage(self, sql_code: str, db_model: Optional[DbModel] = None) -> ApiResponse:
        payload = {"code": sql_code}
        if db_model:
            payload["dbModel"] = db_model.model_dump_json()

        response = requests.post(self.BASE_URL, json=payload, headers=self.headers)
        response.raise_for_status()

        data = response.json()
        return ApiResponse(**data)
