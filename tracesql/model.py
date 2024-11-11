from typing import List

from pydantic import BaseModel, Field


def to_camel(string: str) -> str:
    string_split = string.split("_")
    return string_split[0] + "".join(word.capitalize() for word in string_split[1:])


class BaseSchema(BaseModel):
    class Config:
        alias_generator = to_camel

class SourcePosition(BaseSchema):
    start_idx: int
    end_idx: int

class Dataflow(BaseSchema):
    source_table_id: str
    source_column_name: str
    target_table_id: str
    target_column_name: str
    source_positions: List[SourcePosition]

class Table(BaseSchema):
    table_id: str
    table_name: str
    schema_name: str
    database_name: str
    columns: List[str]
    type_: str = Field(alias="_type")

class Lineage(BaseSchema):
    tables: List[Table]
    dataflows: List[Dataflow]
    input: str

class ApiResponse(BaseSchema):
    lineage: Lineage = Field(alias="jsonLineage")
    svg: str = Field(alias="svgLineage")
