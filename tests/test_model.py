from tracesql.model import ApiResponse

RESPONSE = {
    "jsonLineage": {
        "tables": [
            {
                "tableId": "DEFAULT.DEFAULT.B",
                "tableName": "B",
                "schemaName": "DEFAULT",
                "databaseName": "DEFAULT",
                "columns": ["A"],
                "_type": "UnknownTableType",
            },
            {
                "tableId": "DEFAULT.DEFAULT.ASD",
                "tableName": "ASD",
                "schemaName": "DEFAULT",
                "databaseName": "DEFAULT",
                "columns": ["A"],
                "_type": "Table",
            },
        ],
        "dataflows": [
            {
                "sourceTableId": "DEFAULT.DEFAULT.B",
                "sourceColumnName": "A",
                "targetTableId": "DEFAULT.DEFAULT.ASD",
                "targetColumnName": "A",
                "sourcePositions": [{"startIdx": 34, "endIdx": 35}, {"startIdx": 27, "endIdx": 28}],
            }
        ],
        "input": "create table asd as select a from b;",
    },
    "svgLineage": "",
}


def test_response_load():
    a = ApiResponse(**RESPONSE)
    assert len(a.lineage.dataflows) == 1
    assert len(a.lineage.tables) == 2
