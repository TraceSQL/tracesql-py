from tracesql import analyze_lineage
from tracesql.model import DbModel, DbModelTable

if __name__ == "__main__":
    db_model = DbModel(tables=[DbModelTable(name="CLIENTS", columns=["A", "B", "C"])])
    response = analyze_lineage("select * from CLIENTS;", db_model=db_model)

    with open("image.svg", "w") as fw:
        fw.write(response.svg)

    with open("lineage.json", "w") as fw:
        fw.write(response.lineage.model_dump_json(indent=2))

    print("Lineage successfully saved in files.")
