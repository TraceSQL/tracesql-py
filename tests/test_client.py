import pytest
import requests
import responses

from tracesql.client import TraceSQLClient
from tracesql.model import ApiResponse


@pytest.fixture
def client():
    # Fixture to initialize the client
    return TraceSQLClient(api_key="test_api_key")


@pytest.fixture
def mock_sql_code():
    return "create table asd as select a from b;"


@pytest.fixture
def mock_api_response():
    # Example of the expected JSON response structure
    return {
        "jsonLineage": {
            "tables": [
                {
                    "tableId": "DEFAULT.DEFAULT.B",
                    "tableName": "B",
                    "schemaName": "DEFAULT",
                    "databaseName": "DEFAULT",
                    "columns": ["A"],
                    "_type": "UnknownTableType",
                }
            ],
            "dataflows": [
                {
                    "sourceTableId": "DEFAULT.DEFAULT.B",
                    "sourceColumnName": "A",
                    "targetTableId": "DEFAULT.DEFAULT.ASD",
                    "targetColumnName": "A",
                    "sourcePositions": [{"startIdx": 34, "endIdx": 35}],
                }
            ],
            "input": "create table asd as select a from b;",
        },
        "svgLineage": "",
    }


@responses.activate
def test_analyze_lineage_success(client, mock_sql_code, mock_api_response):
    # Mock the API response with a 200 OK
    responses.add(responses.POST, TraceSQLClient.BASE_URL, json=mock_api_response, status=200)

    # Call the method
    result = client.analyze_lineage(mock_sql_code)

    # Assertions
    assert result is not None
    assert isinstance(result, ApiResponse)
    assert result.lineage.tables[0].table_id == "DEFAULT.DEFAULT.B"
    assert result.lineage.dataflows[0].source_column_name == "A"


@responses.activate
def test_analyze_lineage_http_error(client, mock_sql_code):
    # Mock a 400 Bad Request response
    responses.add(
        responses.POST, TraceSQLClient.BASE_URL, json={"error": "Bad Request"}, status=400
    )

    # Call the method and expect an HTTPError
    with pytest.raises(requests.exceptions.HTTPError):
        client.analyze_lineage(mock_sql_code)


@responses.activate
def test_analyze_lineage_validation_error(client, mock_sql_code):
    # Mock an incomplete or invalid API response that will cause a validation error
    invalid_response = {"invalid_field": "invalid_value"}
    responses.add(responses.POST, TraceSQLClient.BASE_URL, json=invalid_response, status=200)

    # Call the method and expect a ValidationError
    with pytest.raises(ValueError):
        client.analyze_lineage(mock_sql_code)
