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
