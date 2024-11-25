from typing import Optional

import requests

from tracesql.model import ApiResponse


class TraceSQLClient:
    BASE_URL = "https://tracesql.com/api/analyze"

    def __init__(self, api_key: Optional[str] = None):
        self.headers = {
            "Content-Type": "application/json",
        }
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"

    def analyze_lineage(self, sql_code: str) -> Optional[ApiResponse]:
        payload = {"code": sql_code}

        response = requests.post(self.BASE_URL, json=payload, headers=self.headers)
        response.raise_for_status()  # Raises an HTTPError for non-200 responses

        # Parse the JSON response to the ApiResponse model
        data = response.json()
        return ApiResponse(**data)
