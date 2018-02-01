import yaml
from pip import logger

from bin.projectconfiguration import ProjectConf


class FileLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def getData(self):
        with open(self.file_path) as stream:
            try:
                tmp = (yaml.safe_load(stream))
                if tmp is None:
                    raise Exception('There was a problem during loading the configuration file')
                return tmp
            except Exception as exc:
                logger.error(exc)
                logger.error(self.file_path)
                exit(1)



class DefaultConfig:
    data = FileLoader(ProjectConf().get_default_conf_file_path())

    @staticmethod
    def getDefaultDatabaseConfig():
        return DefaultConfig.data.getData().get('database')

    @staticmethod
    def getDefaultMysqlMonitorConfig():
        return DefaultConfig.data.getData().get('mysql_monitor')
