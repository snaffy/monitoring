import argparse
import glob
import os

from bin.configurator.configurator import DbiParser, MysqlMonitorConfig, FileCountConfig
from bin.projectconfiguration import ProjectConf


class Collectd:
    def __init__(self, input_base_path, output_base_path):
        self.input_base_path = input_base_path
        self.output_base_path = output_base_path
        self.host_name = os.path.basename(os.path.normpath(input_base_path))

    def generate_dbi_conf(self):
        in_f_path = os.path.join(self.input_base_path, "dbi_value.yaml")
        out_f_path = os.path.join(self.output_base_path, "plugin_dbi.conf")
        data_to_save = DbiParser.pare_data(in_f_path).getConfiguration()
        self.write_conf_to_file(out_f_path, data_to_save)

    def generate_mysql_conf(self):
        in_f_path = os.path.join(self.input_base_path, "mysql.yaml")
        out_f_path = os.path.join(self.output_base_path, "plugin_mysql.conf")
        data_to_save = MysqlMonitorConfig(in_f_path, self.host_name).getConfiguration()
        self.write_conf_to_file(out_f_path, data_to_save)

    def generate_file_count_conf(self):
        in_f_path = os.path.join(self.input_base_path, "filecount_value.yaml")
        out_f_path = os.path.join(self.output_base_path, "plugin_filecount.conf")
        data_to_save = FileCountConfig(in_f_path).getConfiguration()
        self.write_conf_to_file(out_f_path, data_to_save)

    def write_conf_to_file(self, path, data):
        file = open(path, "w")
        file.write(data)
        file.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate collectd conf')
    parser.add_argument('-ins', help='Instance path')
    args = parser.parse_args()
    conf = ProjectConf()
    config = Collectd(args.ins, conf.get_additional_config_path())
    # TODO do zrobienia ostatni człon ścieżki
    if args.ins:
        if os.path.exists(args.ins):
            for file in glob.glob(os.path.join(args.ins, "*.yaml")):
                if os.path.basename(os.path.normpath(file)) == "dbi_value.yaml":
                    config.generate_dbi_conf()
                if os.path.basename(os.path.normpath(file)) == "filecount_value.yaml":
                    config.generate_file_count_conf()
                if os.path.basename(os.path.normpath(file)) == "mysql.yaml":
                    config.generate_mysql_conf()