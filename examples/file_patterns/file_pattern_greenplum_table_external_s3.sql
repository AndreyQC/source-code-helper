/*====================================================================================
[<[autodoc-yaml]]
object:
  object_catalog: gp_db
  object_key: database/gp_db/schema/${gp_db_ext_schema_name_02}/table/ext_${object_name}
  object_name: ext_${object_name}
  object_schema: ${gp_db_ext_schema_name_02}
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

DROP EXTERNAL TABLE IF EXISTS ${gp_db_ext_schema_name_02}.ext_${object_name} CASCADE;

CREATE EXTERNAL TABLE ${gp_db_ext_schema_name_02}.ext_${object_name} (
    ${greenplum_s3_external_table_column_list}
)
LOCATION ('pxf://${S3_Bucket}/${s3_folder}/ext_${object_name}.csv/?PROFILE=s3:text&accesskey=${S3_AccessKey}&secretkey=${S3_SecretKey}&endpoint=${S3_Endpoint}')
FORMAT 'CSV' (DELIMITER ',' HEADER)
ENCODING 'UTF8';