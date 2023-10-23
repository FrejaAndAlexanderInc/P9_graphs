import configparser
from google.oauth2 import service_account
from pathlib import Path

class Config:
    project_id = None
    database = None
    connection = None

    @classmethod
    def initialize(cls, file_path: str):
        conf = cls.read_conf(file_path)
        cls.project_id = conf.get('mimiciv', 'project_id')
        cls.database = conf.get('mimiciv', 'database')
        cls.connection = cls.__get_gbq_connection()

    @staticmethod
    def read_conf(file_path: str) -> configparser.ConfigParser:
        conf = configparser.ConfigParser()
        read_count = conf.read(file_path)
        if len(read_count) == 0:
            raise Exception(f"Could not read dataset module config.ini file. Path: {file_path}")
        else:
            return conf

    @staticmethod
    def __get_gbq_connection():
        print(Path(__file__).parent.joinpath('service_account.json').resolve())
        return service_account.Credentials.from_service_account_file(
            Path(__file__).parent.joinpath('service_account.json').resolve()
        )