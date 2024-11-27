from tracesql.client import TraceSQLClient
from tracesql.model import DbModel


def analyze_lineage(code: str, db_model: DbModel | None):
    client = TraceSQLClient()
    return client.analyze_lineage(code, db_model=db_model)
