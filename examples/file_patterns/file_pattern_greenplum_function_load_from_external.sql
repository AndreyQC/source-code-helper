/*====================================================================================
[<[autodoc-yaml]]
object:
  object_catalog: gp_db
  object_key: database/gp_db/schema/${gp_db_schema_name_01}/function/fun_${object_type}_${object_name}_load
  object_name: fun_${object_type}_${object_name}_load
  object_schema: ${gp_db_schema_name_01}
  object_type: function
project:
  bild: true
  modules:
  - ${module}
remarks:
  author: ${author}
  task: ${task}
[[autodoc-yaml]>]
=====================================================================================*/

CREATE OR REPLACE FUNCTION ${gp_db_schema_name_01}.fun_${object_type}_${object_name}_load()
RETURNS VOID
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN

    TRUNCATE TABLE ${gp_db_schema_name_01}.${object_type}_${object_name};

    INSERT INTO ${gp_db_schema_name_01}.${object_type}_${object_name} (
        ${greenplum_simple_select_column_list}
    )
    SELECT
        ${greenplum_s3_external_select_column_list_with_alias}
    FROM
        ${gp_db_ext_schema_name_02}.ext_${object_name} AS src;

    ANALYZE ${gp_db_schema_name_01}.${object_type}_${object_name};
END;
$$;
