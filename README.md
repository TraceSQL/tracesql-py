# TraceSQL Python Package

The `tracesql` Python package allows you to connect to the [TraceSQL](https://tracesql.com) server and analyze SQL code for lineage. This package can generate lineage data and provide a downloadable SVG image of the lineage for visualization.

## Features

- Connects to TraceSQL API.
- Analyzes SQL code to generate data lineage.
- Outputs the lineage in JSON format.
- Generates an SVG image of the lineage.

## Installation

You can install the `tracesql` package via pip:

```bash
pip install tracesql
```

## Usage

### Simple example
```python
from tracesql import analyze_lineage

code = """
CREATE TABLE active_customers AS
SELECT customer_id, first_name || ' ' || last_name as fullname, email
FROM customers
WHERE status = 'active';
"""
response = analyze_lineage(code)

# Save the SVG image of the lineage
with open("image.svg", "w") as fw:
    fw.write(response.svg)

# Save the lineage data in JSON format
with open("lineage.json", "w") as fw:
    fw.write(response.lineage.model_dump_json(indent=2))

print("Lineage successfully saved in files.")
```

Here is output for this example:
![simple](examples/output/image.svg)

### Parameters

- `query (str)`: The SQL query whose lineage you want to analyze.
- `db_model (DbModel)`: The database model containing the tables and columns used in the SQL query.

### Response
- `svg`: A string representing the SVG image of the lineage.
- `lineage`: An object containing the lineage data in a pydantic class.
