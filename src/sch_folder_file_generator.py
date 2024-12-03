from yaml import safe_load
import csv
from os import path, getcwd, listdir, makedirs, walk
import shutil
import sch_replace_generator as repgen
import re


# set up paths
FOLDER_FILE_TEMPLATE_PATH = path.join(path.dirname(path.abspath(__file__)), "folder_file_templates")
FILE_PATTERN_PATH = path.join(path.dirname(path.abspath(__file__)), "file_patterns")
REPLACE_TEMPLATE_PATH = path.join(path.dirname(path.abspath(__file__)), "replace_templates")
DATASET_DEFINITION_PATH = path.join(path.dirname(path.abspath(__file__)), "dataset_definition")
FLAG_CLEANUP_TARGET_FOLDER = False


selected_folder_template = path.join(FOLDER_FILE_TEMPLATE_PATH, "db_objects_template_GP_CH.yaml")
selected_replace_template = path.join(REPLACE_TEMPLATE_PATH, "replace_template_01.yaml")
selected_dataset_definition = path.join(DATASET_DEFINITION_PATH, "fixed_costs_mapping_cc__description.csv")


target_folder = path.join(r"C:\Temp\Danone")


new_paths = list()

new_folder_list = list()
new_file_list = list()
file_patterns = dict()


def get_replace_placeholders(template_string):
    """function search all string of the following pattern
        ex ${object_name}
        collect only unique occurrences
    Args:
        template_string (string): string for review
    Returns:
        dict: ex {"object_name":"${object_name}"}
    """
    pattern = r'\$\{([a-zA-Z0-9_]+)\}'
    matches = re.finditer(pattern, template_string)
    result = {}
    for match in matches:
        result[match.group(1)] = match.group(0)
    return result


def get_files_by_path(input_path):
    """
    function accept path
    :param string: path
    :return: array of dictionaries
    """
    list_of_files = []
    files_result = []
    for root, dirs, files in walk(input_path):
        for file in files:
            list_of_files.append(path.join(root, file))
    for name in list_of_files:
        files_result.append(get_file_info(name))
    return files_result


def get_file_info(file_full_path):
    """
    function accept file full path and return parsed dict
    :param string: file_full_path
    :return: dict
    """
    file_path, file_extension = path.splitext(file_full_path)
    file_info = dict()
    file_info['file_name'] = path.basename(file_full_path).split('.')[0]
    file_info['file_dir_name'] = path.dirname(file_full_path)
    file_info['folders'] = file_info['file_dir_name'].split("\\")
    file_info['file_extension'] = file_extension
    file_info['file_full_path'] = file_full_path
    return file_info


def replace_placeholders(template_string,
                         replace_rules,
                         replace_placeholders,
                         input_dataset_definition):
    for k, v in replace_placeholders.items():
        if k in replace_rules.keys():
            if replace_rules[k] == "generated_by_function_from_dataset_definition":
                template_string = template_string.replace(v, repgen.column_list_generator_dict[k](input_dataset_definition))
            else:
                template_string = template_string.replace(v, replace_rules[k])
        else:
            print(f"INFO : there is no replacement rule for  key=[{k}] skipped!")

    return template_string


def add_file_info_to_list(input_k, input_v, input_path):
    new_file = {**input_v, "path": input_path}
    new_file_list.append(new_file)
    # print(f" review file info key=[{input_k}] value [{input_v}] in path [{input_path}]")


def get_folders_and_files(d, top_path=""):
    for k, v in d.items():
        if isinstance(v, dict):
            get_folders_and_files(v, path.join(top_path, k))
            if k == "create_file":
                add_file_info_to_list(k, v, path.join(top_path))
            else:
                new_folder_list.append(path.join(top_path, k))
        else:
            if not v:
                if k == "create_file":
                    add_file_info_to_list(k, v, path.join(top_path))
                else:
                    new_folder_list.append(path.join(top_path, k))


def get_data_from_yaml(input_path):
    with open(input_path, "r", encoding="utf-8") as stream:
        data = safe_load(stream)
    return data


def apply_replace_rules_to_file_list(input_replace_rules):
    for f in new_file_list:
        f["name"] = replace_placeholders(f["name"],
                                         input_replace_rules,
                                         get_replace_placeholders(f["name"]),
                                         dict())


def apply_replace_rules_to_file(input_file_path, input_replace_rules, input_dataset_definition):
    with open(input_file_path) as f:
        s = f.read()
        placeholders = get_replace_placeholders(s)
        if placeholders:
            s = replace_placeholders(s,
                                     input_replace_rules,
                                     get_replace_placeholders(s),
                                     input_dataset_definition)
        else:
            return

    # Safely write the changed content, if found in the file
    with open(input_file_path, 'w', encoding="utf-8") as f:
        print("------ Changing {input_file_path}".format(**locals()))
        f.write(s)


def create_folders(input_folder_list, input_target_folder):
    res = False
    if FLAG_CLEANUP_TARGET_FOLDER:
        if path.exists(input_target_folder) and path.isdir(input_target_folder):
            shutil.rmtree(input_target_folder)
            print(f"INFO: folder {input_target_folder} was recreated")
    for f in input_folder_list:
        try:
            makedirs(path.join(input_target_folder, f), exist_ok=True)
            print(f"INFO: folder {path.join(input_target_folder, f)} was created")
        except Exception:
            res = False

    return res


def get_file_pattern(input_file_pattern_path):
    file_pattern_dict = dict()
    pattern_files = [f for f in get_files_by_path(input_file_pattern_path)]
    for f in pattern_files:
        file_pattern_dict[f["file_name"]] = f
    return file_pattern_dict


def create_files(input_file_list,
                 input_file_pattern_dict,
                 input_target_folder,
                 input_replace_rules,
                 input_dataset_definition):
    for f in input_file_list:
        new_file_name = f["name"]
        new_file_path = path.join(input_target_folder, f["path"])
        new_file_copy_from = input_file_pattern_dict[f["pattern"]]["file_full_path"]
        print(f"INFO: file {new_file_name} will be created in {new_file_path} using pattern {new_file_copy_from}")

        source = path.join(new_file_copy_from)
        destination = path.join(new_file_path, new_file_name)
        try:
            shutil.copy(source, destination)
            print("File copied successfully.")
        # If source and destination are same
        except shutil.SameFileError:
            print("Source and destination represents the same file.")
        # If there is any permission issue
        except PermissionError:
            print("Permission denied.")
        # For other errors
        except Exception:
            print("Error occurred while copying file.")
        apply_replace_rules_to_file(
            destination, input_replace_rules, input_dataset_definition)


def get_data_set_definition(input_ds_definition):
    data_set_definition = repgen.get_dataset_definition(input_ds_definition)
    return data_set_definition


if __name__ == '__main__':
    folder_template = get_data_from_yaml(selected_folder_template)
    replace_rules = get_data_from_yaml(selected_replace_template)
    file_patterns = get_file_pattern(FILE_PATTERN_PATH)
    data_set_definition = get_data_set_definition(selected_dataset_definition)

    get_folders_and_files(folder_template)
    # sort list of folders to create folders in correct order
    new_folder_list.sort()
    apply_replace_rules_to_file_list(replace_rules)
    print("-----------------------------------------------------------------")
    for f in new_folder_list:
        print(f)
    print("-----------------------------------------------------------------")
    for f in new_file_list:
        print(f)

    create_folders(new_folder_list, target_folder)
    create_files(new_file_list, file_patterns, target_folder, replace_rules, data_set_definition)
