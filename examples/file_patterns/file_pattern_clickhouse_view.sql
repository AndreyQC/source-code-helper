/*====================================================================================
[<[autodoc-yaml]]
object:
  object_catalog: CLICKHOUSE_DM_DATABASE
  object_key: database/CLICKHOUSE_DM_DATABASE/view/V_${OBJECT_TYPE_CH}_${OBJECT_NAME}
  object_name: V_${OBJECT_TYPE_CH}_${OBJECT_NAME}
  object_type: view
project:
  bild: true
  modules:
  - ${module}
remarks:
  author: ${author}
  task: ${task}
[[autodoc-yaml]>]
=====================================================================================*/

CREATE OR REPLACE VIEW CLICKHOUSE_DM_DATABASE.V_${OBJECT_TYPE_CH}_${OBJECT_NAME}
AS
SELECT
    ${clickhouse_create_view_column_list}
FROM cis.${object_type}_${object_name} AS dm;
