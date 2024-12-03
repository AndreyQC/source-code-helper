/*====================================================================================
[<[autodoc-yaml]]
object:
  object_catalog: gp_db
  object_key: database/gp_db/schema/ch_gp_db/table/ext_w_staging_${object_type}_${object_name}
  object_name: ext_w_staging_${object_type}_${object_name}
  object_schema: ch_gp_db
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

DROP EXTERNAL TABLE IF EXISTS ch_gp_db.ext_w_staging_${object_type}_${object_name} CASCADE;

CREATE WRITABLE EXTERNAL TABLE ch_gp_db.ext_w_staging_${object_type}_${object_name} (
    ${greenplum_clickhouse_external_table_column_list}
)
LOCATION ('pxf://staging_${object_type}_${object_name}?PROFILE=JDBC&SERVER=ch_gp_db')
FORMAT 'CUSTOM' (FORMATTER='pxfwritable_export')
ENCODING 'UTF8';
