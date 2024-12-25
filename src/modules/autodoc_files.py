import os
import yaml


def get_files_by_path(path):
    """
    function accept path
    :param string: path
    :return: array of dictinaries
    """
    list_of_files = []
    files_result = []
    for root, dirs, files in os.walk(path):
        for file in files:
            list_of_files.append(os.path.join(root, file))
    for name in list_of_files:
        files_result.append(get_file_info(name))
    return files_result


def get_objects_by_autodoc_in_files_by_path(input_path):
    """
    function accept path
    :param string: path
    :return: array of dictionaries with autodoc
    """
    list_of_auto_doc = []
    files_result = get_files_by_path(input_path)

    for f in files_result:
        auto_doc = get_autodoc_yaml_from_file(f["file_full_path"])
        # if there is autodoc
        if "object_status" not in auto_doc["object"].keys():
            auto_doc["file_info"] = f
            print(auto_doc)
            list_of_auto_doc.append(auto_doc)

    return list_of_auto_doc


def get_autodoc_yaml_from_file(path):
    result = {"object": {"object_status": "Not defined AUTODOC YAML", "object_type": {}}, "project": {}}
    search_left_str = "[<[autodoc-yaml]]"
    search_right_str = "[[autodoc-yaml]>]"
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = file.read()
            if search_left_str not in data:
                return result
            elif search_right_str not in data:
                return result

        yaml_start = data.index(search_left_str)
        yaml_end = data.index(search_right_str)
        str_for_yaml = data[yaml_start + 1 + len(search_left_str):yaml_end - 1]
        result = yaml.safe_load(str_for_yaml)
    except Exception as e:
        result = {"object": {"object_status": "Not defined AUTODOC YAML", "object_type": {}}, "project": {}}
    return result


def get_object_container_from_file_path(file_path):
    container_list = ["greenplum", "airflow", "formit", "clickhouse"]
    res = "undefined container"
    for ct in container_list:
        if ct in file_path.lower():
            res = ct
    return res


def get_object_name_with_schema(object_schema: str, object_name:str ) -> str:
    res = object_name
    if object_schema != "none":
        res = object_schema + "." + object_name
    return res


def get_objects_for_report(input_auto_doc):
    report_objects = []
    wrong_objects = []

    for ob in input_auto_doc:
        ro = dict()
        if "object_key" in ob["object"]:
            try:
                ro["object_key"] = ob["object"]["object_key"]
                ro["object_name"] = ob["object"]["object_name"]
                ro["object_schema"] = ob["object"].get("object_schema", "none")
                ro["object_type"] = ob["object"].get("object_type", "none")
                ro["object_container"] = get_object_container_from_file_path(ob["file_info"].get("file_full_path", "none"))
                ro["object_name_with_schema"] = get_object_name_with_schema(ro["object_schema"], ro["object_name"])
                ro["object_modules"] = list(ob.get("project", {}).get("modules", []))
                ro["description"] = ob.get("remarks", {}).get("description", "")
                ro["task"] = ob.get("remarks", {}).get("task", "")
                report_objects.append(ro)
            except KeyError:
                wrong_objects.append(ob)
        else:
            wrong_objects.append(ob)
    return report_objects, wrong_objects


def get_file_info(file_full_path):
    """
    function accept file full path and return parsed dict
    :param string: file_full_path
    :return: dict
    """
    file_path, file_extension = os.path.splitext(file_full_path)
    file_info = dict()
    file_info['file_name'] = os.path.basename(file_full_path)
    file_info['file_dir_name'] = os.path.dirname(file_full_path)
    file_info['file_extension'] = file_extension
    file_info['file_full_path'] = file_full_path
    return file_info


def get_objects_for_report_from_auto_doc(path: str) -> list:
    objects = get_objects_by_autodoc_in_files_by_path(path)
    report_objects, _ = get_objects_for_report(objects)
    return report_objects


def get_objects_for_report_from_auto_doc_filtered_by_module(path: str, module_filter: list) -> list:
    objects = get_objects_by_autodoc_in_files_by_path(path)
    report_objects, _ = get_objects_for_report(objects)
    if len(module_filter) == 0:
        res = report_objects
    else:
        res = [f for f in report_objects if any(x in f["object_modules"] for x in module_filter)]
    return res


if __name__ == '__main__':

    path = r"C:\repos\Danone\NewBI\newbi-backend\Airflow\dags\danone\dags\processing"
    # path = "C:\\Users\\Andrey_Potapov\\Nextcloud\\Localization BI\\WAVE 2 Localization\\SALES.CRPT\\04 source code for MR"
    print(path)

    # example how to filter files by extension
    # files_sql = [f for f in get_files_by_path(path) if f['file_extension'] == '.sql']
    module_filter = "CRPT"
    module_list = module_filter.split(",")

    report_objects = get_objects_for_report_from_auto_doc_filtered_by_module(path, module_list)
    if report_objects:
        for r in report_objects:
            print(r)
