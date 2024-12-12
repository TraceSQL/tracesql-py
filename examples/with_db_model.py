from tracesql import analyze_lineage
from tracesql.model import DbModel, DbModelTable

code = """
CREATE TABLE ACTIVE_CUSTOMERS AS
SELECT *
FROM CUSTOMERS;
"""
db_model = DbModel(
    tables=[
        DbModelTable(
            name="ACTIVE_CUSTOMERS", columns=["customer_id", "full_name", "email", "status"]
        ),
        DbModelTable(name="CUSTOMERS", columns=["customer_id", "full_name", "email", "status"]),
    ]
)
response = analyze_lineage(code, db_model=db_model)

# Save the SVG image of the lineage
with open("image.svg", "w") as fw:
    fw.write(response.svg)

# Save the lineage data in JSON format
with open("lineage.json", "w") as fw:
    fw.write(response.lineage.model_dump_json(indent=2))

print("Lineage successfully saved in files.")
