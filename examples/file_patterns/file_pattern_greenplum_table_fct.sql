/*====================================================================================
[<[autodoc-yaml]]
object:
  object_catalog: gp_db
  object_key: database/gp_db/schema/${gp_db_schema_name_01}/table/${object_type}_${object_name}
  object_name: ${object_type}_${object_name}
  object_schema: ${gp_db_schema_name_01}
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

DROP TABLE IF EXISTS ${gp_db_schema_name_01}.${object_type}_${object_name} CASCADE;

CREATE TABLE ${gp_db_schema_name_01}.${object_type}_${object_name} (
    ${greenplum_create_table_column_list}
)
WITH
(
    APPENDOPTIMIZED = TRUE,
    ORIENTATION = COLUMN,
    COMPRESSTYPE = ZSTD,
    COMPRESSLEVEL = 1
)
DISTRIBUTED RANDOMLY;
