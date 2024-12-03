from yaml import safe_load
import logging
from os import path, getcwd, listdir, makedirs, walk
import shutil
import re


# set up paths
FOLDER_FILE_TEMPLATE_PATH = path.join(path.dirname(path.abspath(__file__)), "folder_file_templates")
FILE_PATTERN_PATH = path.join(path.dirname(path.abspath(__file__)), "file_patterns")
REPLACE_TEMPLATE_PATH = path.join(path.dirname(path.abspath(__file__)), "replace_templates")
DATASET_DEFINITION_PATH = path.join(path.dirname(path.abspath(__file__)), "replace_templates")
FLAG_CLEANUP_TARGET_FOLDER = True


selected_folder_template = path.join(FOLDER_FILE_TEMPLATE_PATH, "db_objects_template_GP_CH.yaml")
selected_replace_template = path.join(REPLACE_TEMPLATE_PATH, "replace_template_01.yaml")
target_folder = path.join(r"C:\Temp\Danone")


newpaths = list()

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


def replace_placeholders(template_string, replace_rules, replace_placeholders):
    for k, v in replace_placeholders.items():
        template_string = template_string.replace(v, replace_rules[k])
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
    with open(input_path, "r") as stream:
        data = safe_load(stream)
    return data


def apply_replace_rules_to_file_list(input_replace_rules):
    for f in new_file_list:
        f["name"] = replace_placeholders(f["name"],
                                         input_replace_rules,
                                         get_replace_placeholders(f["name"]))


def apply_replace_rules_to_file(input_file_path, input_replace_rules):
    with open(input_file_path) as f:
        s = f.read()
        placeholders = get_replace_placeholders(s)
        if placeholders:
            s = replace_placeholders(s,
                                     input_replace_rules,
                                     get_replace_placeholders(s))
        else:
            return

    # Safely write the changed content, if found in the file
    with open(input_file_path, 'w') as f:
        print("Changing {input_file_path}".format(**locals()))
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
                 input_replace_rules):
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
            apply_replace_rules_to_file(destination, input_replace_rules)
        # If source and destination are same
        except shutil.SameFileError:
            print("Source and destination represents the same file.")
        # If there is any permission issue
        except PermissionError:
            print("Permission denied.")
        # For other errors
        except Exception:
            print("Error occurred while copying file.")


if __name__ == '__main__':

