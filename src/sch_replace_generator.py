import csv
from os import path


data_set_definition = list()


def get_dataset_definition(input_path):
    res = list()
    with open(input_path, encoding="utf-8") as f:
        res = [{k: v for k, v in row.items()}
               for row in csv.DictReader(f, skipinitialspace=True, delimiter=";")]
    return res


def get_clickhouse_create_table_column_list(input_dataset_definition):
    """_summary_
    create the following output
    ----------------------------
    `budget_group` TEXT NULL,
    `budget_group_ri` TEXT NULL,
    `cost_element_name` TEXT NULL,
    `cost_line_ri` TEXT NULL,
    `gl_account` TEXT NULL,
    `magnitude_code` TEXT NULL,
    `magnitude_name` TEXT NULL,
    `reporting_line` TEXT NULL
    """
    s = ',\n    '
    column_names = ["`" + d['ch_column_name'] + "`" for d in input_dataset_definition if 'ch_column_name' in d]
    column_types = [d['ch_column_data_type'] + " NULL" for d in input_dataset_definition if 'ch_column_data_type' in d]
    zipped_lists = list(zip(column_names, column_types))
    mapped_strings = list(map(lambda x: " ".join(x), zipped_lists))
    # mapped_strings = list(map(lambda x, y: f"{x} {y}", *zipped_lists))
    return s.join(mapped_strings)


def get_greenplum_s3_external_table_column_list_with_alias(input_dataset_definition):
    """_summary_
    create the following output
    ----------------------------
    src."Actual_Costs",
    src."AR Line",
    src."Actual_Secodary_Costs",
    src."Business Area",
    """
    s = ',\n        '
    column_names = ["src.\"" + d['file_column_name'] + "\"" for d in input_dataset_definition if 'file_column_name' in d]
    return s.join(column_names)


def get_greenplum_s3_external_select_column_list(input_dataset_definition):
    """_summary_
    create the following output
    ----------------------------
    "Actual_Costs" TEXT,
    "AR Line" TEXT,
    "Actual_Secodary_Costs" TEXT,
    "Business Area" NUMERIC(38, 0),
    """
    s = ',\n    '
    column_names = ["\"" + d['file_column_name'] + "\"" for d in input_dataset_definition if 'file_column_name' in d]
    column_types = [d['file_column_data_type'] for d in input_dataset_definition if 'file_column_data_type' in d]
    zipped_lists = list(zip(column_names, column_types))
    mapped_strings = list(map(lambda x: " ".join(x), zipped_lists))
    # mapped_strings = list(map(lambda x, y: f"{x} {y}", *zipped_lists))
    return s.join(mapped_strings)


def get_clickhouse_create_view_column_list(input_dataset_definition):
    """_summary_
        create the following output
    ----------------------------
    dm.`actual_costs` AS `actual_costs`,
    dm.`ar_line` AS `ar_line`,
    dm.`actual_secodary_costs` AS `actual_secodary_costs`,
    """
    s = ',\n    '
    column_names = ["dm.`" + d['ch_column_name'] + "` AS `" + d['ch_view_column_name'] + "`" for d in input_dataset_definition if 'ch_column_name' in d]
    return s.join(column_names)


def get_greenplum_simple_select_column_list(input_dataset_definition):
    """_summary_
        create the following output
    ----------------------------
        budget_group,
        budget_group_ri,
        cost_element_name,
        cost_line_ri,
    """
    s = ',\n        '
    column_names = [d['gp_column_name'] for d in input_dataset_definition if 'gp_column_name' in d]
    return s.join(column_names)


def get_greenplum_create_table_column_list(input_dataset_definition):
    """_summary_
        create the following output
    ----------------------------
    budget_group TEXT NULL,
    budget_group_ri TEXT NULL,
    cost_element_name TEXT NULL,
    """
    s = ',\n    '
    column_names = [d['gp_column_name'] for d in input_dataset_definition if 'gp_column_name' in d]
    column_types = [d['gp_column_data_type'] + " NULL" for d in input_dataset_definition if 'gp_column_data_type' in d]
    zipped_lists = list(zip(column_names, column_types))
    mapped_strings = list(map(lambda x: " ".join(x), zipped_lists))
    # add default
    mapped_strings.append("t_rec_ins_date TIMESTAMP NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'utc')")
    # mapped_strings = list(map(lambda x, y: f"{x} {y}", *zipped_lists))
    return s.join(mapped_strings)


def get_greenplum_clickhouse_external_table_column_list(input_dataset_definition):
    """_summary_
        create the following output
    ----------------------------
    "actual_costs" TEXT,
    "ar_line" TEXT,
    "actual_secodary_costs" TEXT,
    "business_area" NUMERIC(38, 0),
    "business_unit" TEXT,
    """
    s = ',\n    '
    column_names = ["\"" + d['ch_column_name'] + "\"" for d in input_dataset_definition if 'ch_column_name' in d]
    column_types = [d['gp_column_data_type'] for d in input_dataset_definition if 'gp_column_data_type' in d]
    zipped_lists = list(zip(column_names, column_types))
    mapped_strings = list(map(lambda x: " ".join(x), zipped_lists))
    # mapped_strings = list(map(lambda x, y: f"{x} {y}", *zipped_lists))
    return s.join(mapped_strings)


def get_greenplum_select_column_list_with_alias(input_dataset_definition):
    """_summary_
        create the following output
    ----------------------------
        budget_group,
        budget_group_ri,
        cost_element_name,
        cost_line_ri,
    """
    s = ',\n        '
    column_names = ["src.\"" + d['gp_column_name'] + "\"" for d in input_dataset_definition if 'gp_column_name' in d]
    return s.join(column_names)


column_list_generator_dict = {
    "clickhouse_create_table_column_list": get_clickhouse_create_table_column_list,
    "clickhouse_create_view_column_list": get_clickhouse_create_view_column_list,
    "greenplum_s3_external_table_column_list": get_greenplum_s3_external_select_column_list,
    "greenplum_s3_external_select_column_list_with_alias": get_greenplum_s3_external_table_column_list_with_alias,
    "greenplum_simple_select_column_list": get_greenplum_simple_select_column_list,
    "greenplum_create_table_column_list": get_greenplum_create_table_column_list,
    "greenplum_clickhouse_external_table_column_list": get_greenplum_clickhouse_external_table_column_list,
    "greenplum_select_column_list_with_alias": get_greenplum_select_column_list_with_alias
}


if __name__ == '__main__':
    DATASET_DEFINITION_PATH = path.join(path.dirname(path.abspath(__file__)), "dataset_definition")
    selected_dataset_definition = path.join(DATASET_DEFINITION_PATH, "fixed_costs_mapping_cc__description.csv")
    data_set_definition = get_dataset_definition(selected_dataset_definition)
    print(data_set_definition)
    clickhouse_create_table_column_list = column_list_generator_dict["clickhouse_create_table_column_list"](data_set_definition)
    print(clickhouse_create_table_column_list)
