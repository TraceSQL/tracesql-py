
## TOC

- [TraceSQL Python Package](#tracesql-python-package)
  - [Features](#features)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Simple example](#simple-example)
  - [`analyze_lineage` method](#analyze_lineage-method)
    - [Parameters](#parameters)
    - [Response - `ApiResponse`](#response---apiresponse)
- [Data lineage](#data-lineage)
  - [Data lineage in SQL (technical view)](#data-lineage-in-sql-technical-view)
    - [Simple `SELECT`](#simple-select)
    - [Wildcard](#wildcard)
    - [Ambiguous Queries](#ambiguous-queries)



# TraceSQL Python Package

The `tracesql` Python is client for [TraceSQL](https://tracesql.com). It allows you to easily analyze SQL code for data lineage.


You can currently use this client and the API it wraps without any limitations or tokens. This might be changed in the future.


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

## `analyze_lineage` method

It provides the most basic interface for analyzing lineage. Check the underlaying code if you want to build something more capable.

### Parameters

- `query (str)`: The SQL query whose lineage you want to analyze.
- `db_model (Optional[DbModel])`: The database model containing the tables and columns used in the SQL query.

### Response - `ApiResponse`
- `svg`: A string representing the SVG image of the lineage.
- `lineage`: An object containing the lineage data in a pydantic class.


Each relation includes an attribute named `source_positions`, which provides detailed information about code, that is relevant for this relation:
```json
"source_positions": [
    {
        "start_idx": 109,
        "end_idx": 118
    }
    ...
]
```
The `start_idx` and `end_idx` represent character indices in the input SQL code. Together, they define a range that pinpoints the specific section of the code corresponding to the relation. These indices effectively serve as "pointers" to the relevant portion of the analyzed SQL query.


# Data lineage

Lineage traditionally refers to a person’s or group’s ancestry, tracing their origins and heritage through generations. It embodies the historical path that defines their roots and connections.

Similarly, data lineage traces the lifecycle of data, mapping its origins, transformations, and usage. It answers critical questions such as:

- Where did this data originate?
- How is this data used across systems or processes?
- What steps were involved in constructing this data?

More specific examples include:

- Can I safely delete this column?
- Are there scripts or processes that depend on this table?
- Who created or modified this data?

In a world where data is often more valuable than gold, it’s crucial to answer these questions quickly and accurately. This is why data lineage plays a vital role in effective data governance.

## Data lineage in SQL (technical view)

How is lineage created in SQL? It is as simple as creating a table:
```
CREATE TABLE NEW_TABLE
AS SELECT first_name, last_name from OLD_TABLE;
```
With this query, we have create lineage from `OLD_TABLE` to `NEW_TABLE`. On column level, this would look like this:
```
OLD_TABLE.first_name -> NEW_TABLE.first_name
OLD_TABLE.last_name -> NEW_TABLE.last_name
```

Lineage is created whenever data is moved or transformed. In SQL, this typically involves a `SELECT` statement to retrieve data before moving it, making `SELECT` the cornerstone of lineage analysis.

1. **Analyze `targets`** – Identify the destination of the `SELECT` statement, usually a single table.
2. **Analyze `sources`** – Identify the data sources, typically multiple tables referenced in the `FROM` clause.
3. **Connect `sources` and `targets`** – Establish relationships between sources and their corresponding targets.

### Simple `SELECT`

What happens when a `SELECT` statement has no explicit target?

```sql
SELECT name FROM accounts;
```

In most IDEs, this query simply displays the results. To model this behavior in lineage, we create an artificial target called `SELECT-RESULT`:

```
accounts.name -> SELECT-RESULT.name
```

This approach ensures the lineage remains consistent, even without a defined target.


### Wildcard

```sql
SELECT * FROM events;
```

This case is impossible to analyze without any extra info. We need to check the database model - view the columns of table `events`. You can either do this by providing the `CREATE TABLE` statement or you can provide the database model in JSON format directly to the API.


### Ambiguous Queries

Consider the following query:
```sql
SELECT price, name FROM products NATURAL JOIN suppliers;
```
Analyzing lineage in this case is challenging due to the absence of table aliases and fully qualified column names. Without these, it becomes unclear which table each column originates from.

While providing the database model to the lineage analyzer can help resolve this ambiguity, the best practice is to use explicit column references and table aliases to avoid confusion

```sql
SELECT p.price, s.name FROM products p
NATURAL JOIN suppliers sl
```

This approach ensures clearer lineage analysis and reduces the risk of misinterpreting the data's origins.

