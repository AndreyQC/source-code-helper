import csv


def save_csv_from_list_of_dict(list_of_dict: list, path: str) -> None:
    result = dict()
    if len(list_of_dict) == 0:
        result = {"result": "empty"}
    else:
        keys = list_of_dict[0].keys()

        with open(path, 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(list_of_dict)
        result = {"result": "created"}
    return result


if __name__ == '__main__':

    path = r'C:\Users\Andrey_Potapov\Nextcloud\Localization BI\WAVE 2 Localization\SALES.CRPT\report.csv'

    list_of_dict = [
                    {'object_key': 'database/cis/schema/cis_stg_crpt/table/tr_crpt_sales_retail_by_tn_addr', 'object_name': 'tr_crpt_sales_retail_by_tn_addr', 'object_schema': 'cis_stg_crpt', 'object_type': 'table', 'object_container': 'greenplum', 'object_modules': ['CRPT']}, 
    {'object_key': 'database/cis/schema/cis_stg_crpt/table/tr_crpt_turnover_mth', 'object_name': 'tr_crpt_turnover_mth', 'object_schema': 'cis_stg_crpt', 'object_type': 'table', 'object_container': 'greenplum', 'object_modules': ['CRPT']}, 
    {'object_key': 'database/cis/schema/cis_stg_crpt/table/tr_crpt_turnover_wky', 'object_name': 'tr_crpt_turnover_wky', 'object_schema': 'cis_stg_crpt', 'object_type': 'table', 'object_container': 'greenplum', 'object_modules': ['CRPT']}
                    ]

    print(list_of_dict)

    save_csv_from_list_of_dict(list_of_dict, path)