/*====================================================================================
[<[autodoc-yaml]]
object:
  object_catalog: clickhouse_database
  object_key: database/clickhouse_database/table/${object_type}_${object_name}
  object_name: ${object_type}_${object_name}
  object_type: table
project:
  bild: true
  modules:
  - ${module}
remarks:
  author: ${author}
  task: ${task}
[[autodoc-yaml]>]
=====================================================================================*/

CREATE TABLE clickhouse_database.${object_type}_${object_name}
(
    ${clickhouse_create_table_column_list}
)
ENGINE = MergeTree
ORDER BY tuple()
SETTINGS allow_nullable_key = 1;
