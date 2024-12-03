import os
import yaml
import logging


class Config(object):

    def __init__(self, yaml_config_file, is_main=True):
        with open(yaml_config_file) as stream:
            yaml_config = yaml.safe_load(stream)

        self.APP_NAME = "Source_Code_Helper"
        assert self.APP_NAME == yaml_config["app_name"]
        self.APP_SHORT_NAME = yaml_config["app_short_name"]
        self.WORKING_PATH = yaml_config["paths"]["working_path"]
        self.INITIAL_SCRIPT_NAME = "source_code_helper"

        # paths
        self.LOG_PATH = self.VerifyPath(yaml_config["paths"]["log_path"])
        os.makedirs(self.LOG_PATH, exist_ok=True)

    def VerifyPath(self, path, parentPath=None):
        if parentPath is None:
            parentPath = self.WORKING_PATH
        return path if os.path.isabs(path) else os.path.join(parentPath, path)

    def AssertConfig(self):
        assert self.APP_NAME


if __name__ == "__main__":

    config_folder_path = os.path.dirname(os.path.abspath(__file__))
    config = Config(os.path.join(config_folder_path, "config.yaml"))
    logging.info(vars(config))
    config.AssertConfig()
