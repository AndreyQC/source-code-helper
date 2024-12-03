import dearpygui.dearpygui as dpg
import webbrowser
import copy
from dearpygui_ext.themes import create_theme_imgui_dark
import sch_folder_file_generator as ffg
import modules.autodoc_files as auto_doc
import modules.report as auto_doc_report

from yaml import safe_load
from os import path, getcwd, listdir, makedirs

version = "0.1"

templates = []
newpaths = []


def _hyperlink(text, address):
    b = dpg.add_button(label=text, callback=lambda:webbrowser.open(address))
    dpg.bind_item_theme(b, "__demo_hyperlinkTheme")


path_schui = path.dirname(path.abspath(__file__))
path_examples = path.join(path.dirname(path.dirname(path.abspath(__file__))),"examples")
path_file_template = path.join(path_examples,"folder_file_templates")
path_replace_templates = path.join(path_examples,"replace_templates")
path_dataset_definition = path.join(path_examples,"dataset_definition")
path_file_patterns = path.join(path_examples,"file_patterns")
path_assets = path.join(path_schui, "assets")

default_path = r"C:\-=Dump=-"
default_report_file_name = "отчет_по_объектам"


for file in listdir(path_file_template):
    if file.endswith(".yaml"):
        templates.append(file)


def dict_to_dir(data, top_path=""):
    if isinstance(data, dict):
        print(f"--dict  {data}")
        for k, v in data.items():
            dict_to_dir(v, k)
            print(f'call  dict_to_dir ( key= [{k}]  value = [{v}])')
    elif isinstance(data, list):
        print(f"    --list {data} ")
        for i in data:
            if isinstance(i, dict):
                print(f"--dict level 2 {i}")
                for k, v in i.items():
                    dict_to_dir(v, path.join(top_path, k))
                    print(f'call  dict_to_dir ( key= [{k}]  value = [{path.join(top_path, k)}])')

            else:
                newpaths.append(path.join(top_path, i))
                print(f' final path {path.join(top_path, i)}')


dpg.create_context()

with dpg.value_registry():
    dpg.add_string_value(default_value="", tag="value__selected_dataset_definition_file")
    dpg.add_string_value(default_value="", tag="value__selected_replace_template_file")
# with dpg.font_registry():
#     default_font = dpg.add_font(path.join(assets_path,"Akrobat-SemiBold.otf"), 16)
#     dpg.bind_font(default_font)

big_let_start = 0x00C0  # Capital "A" in cyrillic alphabet
big_let_end = 0x00DF  # Capital "Я" in cyrillic alphabet
small_let_end = 0x00FF  # small "я" in cyrillic alphabet
remap_big_let = 0x0410  # Starting number for remapped cyrillic alphabet
alph_len = big_let_end - big_let_start + 1  # adds the shift from big letters to small
alph_shift = remap_big_let - big_let_start  # adds the shift from remapped to non-remapped

with dpg.font_registry():
    with dpg.font(path.join(path_assets, "Akrobat-SemiBold.otf"), 18) as default_font:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
        biglet = remap_big_let  # Starting number for remapped cyrillic alphabet
        for i1 in range(big_let_start, big_let_end + 1):  # Cycle through big letters in cyrillic alphabet
            dpg.add_char_remap(i1, biglet)  # Remap the big cyrillic letter
            dpg.add_char_remap(i1 + alph_len, biglet + alph_len)  # Remap the small cyrillic letter
            biglet += 1  # choose next letter
        dpg.bind_font(default_font)


def callback(_sender, app_data):
    # Set the text field value to selected path
    dpg.set_value("target_path", app_data["current_path"])


def callback_replace_template(_sender, app_data):
    # Set the text field value to selected path
    dpg.set_value("value__selected_replace_template_file", app_data["file_path_name"])
    dpg.set_value("input__file_replace_template",
                  app_data["file_name"])


def callback_dataset_definition(_sender, app_data):
    # Set the text field value to selected path
    dpg.set_value("value__selected_dataset_definition_file", app_data["file_path_name"])
    dpg.set_value("input__file_dataset_definition",
                  app_data["file_name"])


def callback__dialog__path_file_patterns(_sender, app_data):
    # Set the text field value to selected path
    dpg.set_value("input__path_file_patterns", app_data["current_path"])


def callback__dialog__path_objects_for_report(_sender, app_data):
    # Set the text field value to selected path
    dpg.set_value("input__path_objects_for_report", app_data["current_path"])


def callback__dialog__path_report(_sender, app_data):
    # Set the text field value to selected path
    dpg.set_value("input__path_report", app_data["current_path"])


def cancel_callback(_sender, _app_data):
    pass


def callback_button__create_report():
    selected__source_code_path = path.join(dpg.get_value("input__path_objects_for_report"))
    selected__report_path = path.join(dpg.get_value("input__path_report"))
    selected__report_name = path.join(dpg.get_value("input__report_file_name")) + ".csv"
    report__full_path = path.join(selected__report_path,selected__report_name)
    print("-----------------------------------------------------------------")
    print(f"selected__source_code_path {selected__source_code_path}")
    print(f"selected__report_path {selected__report_path}")
    print(f"selected__report_name {selected__report_name}")
    report_objects = auto_doc.get_objects_for_report_from_auto_doc(selected__source_code_path)
    if report_objects:
        for r in report_objects:
            print(r)
    auto_doc_report.save_csv_from_list_of_dict(report_objects, report__full_path)    
    print(report__full_path)


def create_folders():
    # create the folder structure
    selected_folder_template = path.join(path_file_template, dpg.get_value("chosen_template"))
    selected_path_file_patterns = dpg.get_value("input__path_file_patterns")
    target_path = dpg.get_value("target_path")
    folder_template = ffg.get_data_from_yaml(selected_folder_template)
    replace_rules = ffg.get_data_from_yaml(dpg.get_value("value__selected_replace_template_file"))
    dataset_definition = ffg.get_data_set_definition(dpg.get_value("value__selected_dataset_definition_file"))

    file_patterns = ffg.get_file_pattern(selected_path_file_patterns)

    ffg.get_folders_and_files(folder_template)
    # sort list of folders to create folders in correct order
    ffg.new_folder_list.sort()
    ffg.apply_replace_rules_to_file_list(replace_rules)
    print("-----------------------------------------------------------------")
    for f in ffg.new_folder_list:
        print(f)
    print("-----------------------------------------------------------------")
    for f in ffg.new_file_list:
        print(f)

    ffg.create_folders(ffg.new_folder_list, target_path)
    print(ffg.new_file_list)
    ffg.create_files(ffg.new_file_list, file_patterns,
                     target_path, replace_rules, dataset_definition)

    dpg.show_item("modal_id")


with dpg.window(tag="Primary Window", autosize=True):

    with dpg.group(horizontal=True) as directory_group:
        dpg.add_loading_indicator(circle_count=4)
        with dpg.group():
            dpg.add_text(f'Dear PyGui says hello. ({dpg.get_dearpygui_version()})')
            with dpg.group(horizontal=True):
                dpg.add_text("Helper for some routine tasks")

    # подключения к базе
    with dpg.collapsing_header(label="Подключения к базам данных"):
        dpg.add_text("Выберете каталог с конфигурациями подключений")

    # формирование отчета
    with dpg.collapsing_header(label="Сформировать отчет в формате csv по Autodoc"):
        dpg.add_text("Выберете каталог с объектами исходного кода для формирования отчета")
        with dpg.group(horizontal=True):
            dpg.add_input_text(default_value=default_path, tag="input__path_objects_for_report")

            dpg.add_button(
                label="...", callback=lambda: dpg.show_item("dialog__path_objects_for_report")
            )
            dpg.add_file_dialog(
                directory_selector=True,
                show=False,
                callback=callback__dialog__path_objects_for_report,
                tag="dialog__path_objects_for_report",
                cancel_callback=cancel_callback,
                width=600,
                height=500,
                default_path=default_path,
                modal=True,
            )

        dpg.add_text("Выберете каталог, где будет сохранен файл отчета ")
        with dpg.group(horizontal=True):
            dpg.add_input_text(default_value=default_path, tag="input__path_report")

            dpg.add_button(
                label="...", callback=lambda: dpg.show_item("dialog__path_report")
            )
            dpg.add_file_dialog(
                directory_selector=True,
                show=False,
                callback=callback__dialog__path_report,
                tag="dialog__path_report",
                cancel_callback=cancel_callback,
                width=600,
                height=500,
                default_path=default_path,
                modal=True,
            )

        dpg.add_text("Введите наменование файла отчета")
        dpg.add_input_text(default_value=default_report_file_name, tag="input__report_file_name")

        dpg.add_button(label="Сформировать отчет",
                           callback=callback_button__create_report, width=-1, height=50)

    # Генерация файлов для репозитория
    with dpg.collapsing_header(label="Генерация файлов для репозитория"):

        with dpg.tree_node(label="На основе конфигурации:"):
            # Path text field & Directory Selector button
            dpg.add_text("Выберете каталог где будут сгенерированны файлы")
            with dpg.group(horizontal=True):
                dpg.add_input_text(default_value=default_path, tag="target_path")

                dpg.add_button(
                    label="...", callback=lambda: dpg.show_item("file_dialog_id")
                )
                dpg.add_file_dialog(
                    directory_selector=True,
                    show=False,
                    callback=callback,
                    tag="file_dialog_id",
                    cancel_callback=cancel_callback,
                    width=600,
                    height=500,
                    default_path=default_path,
                    modal=True,
                )
            # Path text field & Directory Selector button
            dpg.add_text("Выберете каталог где находятся шаблоны скриптов")
            with dpg.group(horizontal=True):
                dpg.add_input_text(default_value=path_file_patterns, tag="input__path_file_patterns")

                dpg.add_button(
                    label="...", callback=lambda: dpg.show_item("dialog__path_file_patterns")
                )
                dpg.add_file_dialog(
                    directory_selector=True,
                    show=False,
                    callback=callback__dialog__path_file_patterns,
                    tag="dialog__path_file_patterns",
                    cancel_callback=cancel_callback,
                    width=600,
                    height=500,
                    default_path=default_path,
                    modal=True,
                )
        # Template select dropdown
            dpg.add_text("Выберете template по которому будут создаваться папки и файлы")
            dpg.add_combo(
                label="Select Template",
                items=templates,
                default_value=templates[0],
                tag="chosen_template",
            )
        # Replace template
            dpg.add_text("Выберете файл с правилами замен")
            with dpg.group(horizontal=True):
                dpg.add_input_text(default_value="", tag="input__file_replace_template")
                dpg.add_button(
                    label="Choose Replace Template", callback=lambda: dpg.show_item("file_dialog_id_replace_template")
                )
                with dpg.file_dialog(
                    directory_selector=False,
                    show=False,
                    callback=callback_replace_template,
                    tag="file_dialog_id_replace_template",
                    width=700,
                    height=400,
                    default_path=path_replace_templates,
                    modal=True
                ):
                    dpg.add_file_extension(".yaml", color=(150, 255, 150, 255))
        # Dataset Defenition
            dpg.add_text("Выберете файл с описанием датасета")
            with dpg.group(horizontal=True):            
                dpg.add_input_text(default_value="", tag="input__file_dataset_definition")
                with dpg.file_dialog(
                    directory_selector=False,
                    show=False,
                    callback=callback_dataset_definition,
                    id="file_dialog_id_dataset_definition",
                    width=700,
                    height=400,
                    default_path=path_dataset_definition,
                    modal=True
                ):
                    dpg.add_file_extension(".csv", color=(150, 255, 150, 255))
                dpg.add_button(
                    label="Choose Dataset Definition", callback=lambda: dpg.show_item("file_dialog_id_dataset_definition")
                )

            dpg.add_button(label="Create Folders",
                           callback=create_folders, width=-1, height=50)
    dpg.add_text("version " + version)

    # Info message popup
    with dpg.window(
        label="Info",
        modal=True,
        show=False,
        tag="modal_id",
        pos=(300, 200),
        no_resize=True,
        autosize=True,
    ):
        dpg.add_text("Completed", tag="message")
        dpg.add_button(
            label="OK",
            callback=lambda: dpg.configure_item("modal_id", show=False),
            width=-1,
        )


dpg.create_viewport(
    title="Helper " + version,
    width=700,
    height=600,
    decorated=True,
)

dark_theme = create_theme_imgui_dark()
dpg.bind_theme(dark_theme)
dpg.setup_dearpygui()
dpg.set_viewport_large_icon("assets/graphics/appicon.ico")
dpg.set_viewport_small_icon("assets/graphics/appicon.ico")
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()
