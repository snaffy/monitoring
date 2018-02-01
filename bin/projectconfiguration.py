import os


class ProjectConf:
    main_conf_dir_name = 'main-config'
    additional_conf_dir_name = 'additional-config'
    default_conf_name = 'default_conf.yaml'
    dbi_filename = 'dbi_value'
    filename_suffix = '.conf'

    def get_base_path(self):
        return os.path.dirname(os.path.abspath(__file__))

    def get_additional_config_path(self):
        return os.path.join(os.path.dirname(self.get_base_path()), self.additional_conf_dir_name, '')

    def get_main_config_path(self):
        return os.path.join(os.path.dirname(self.get_base_path()), self.main_conf_dir_name, '')

    def get_default_conf_file_path(self):
        return os.path.join(self.get_main_config_path(), self.default_conf_name)
