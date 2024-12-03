/*====================================================================================
[<[autodoc-yaml]]
object:
  object_catalog: gp_db
  object_key: database/gp_db/schema/${gp_db_dsp_per_schema_name}/view/v_${object_type}_${object_name}
  object_name: v_${object_type}_${object_name}
  object_schema: ${gp_db_dsp_per_schema_name}
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

CREATE OR REPLACE VIEW ${gp_db_dsp_per_schema_name}.v_${object_type}_${object_name} (
    ${greenplum_simple_select_column_list}
) AS
SELECT
    ${greenplum_select_column_list_with_alias}
FROM ${gp_db_schema_name_01}.${object_type}_${object_name} AS src;
