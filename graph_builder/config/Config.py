import configparser
from google.oauth2 import service_account
from pathlib import Path

class Config:
    def __init__(self, file_path: str) -> None:
        conf = self.read_conf(file_path)
        self.project_id = conf.get('mimiciv', 'project_id')
        self.database = conf.get('mimiciv', 'database')
        self.connection = self.__get_gbq_connection()

    def read_conf(self, file_path: str) -> configparser.ConfigParser:
        conf = configparser.ConfigParser()
        read_count = conf.read(file_path)
        if len(read_count) == 0:
            raise Exception(f"Could not read dataset module config.ini file. Path: {file_path}")
        else:
            return conf
        
    def __get_gbq_connection(self):
        return service_account.Credentials.from_service_account_file(
            Path(__file__).parent.joinpath('service_account.json').resolve()
        )