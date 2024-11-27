from typing import Optional

from tracesql.client import TraceSQLClient
from tracesql.model import DbModel


def analyze_lineage(code: str, db_model: Optional[DbModel] = None):
    return TraceSQLClient().analyze_lineage(code, db_model=db_model)
