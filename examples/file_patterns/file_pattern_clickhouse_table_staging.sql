/*====================================================================================
[<[autodoc-yaml]]
object:
  object_catalog: clickhouse_database
  object_key: database/clickhouse_database/staging table/staging_${object_type}_${object_name}
  object_name: staging_${object_type}_${object_name}
  object_type: staging table
project:
  bild: true
  modules:
  - ${module}
remarks:
  author: ${author}
  task: ${task}
[[autodoc-yaml]>]
=====================================================================================*/

CREATE TABLE clickhouse_database.staging_${object_type}_${object_name} AS
    clickhouse_database.${object_type}_${object_name};
