import configparser
import json
from google.oauth2 import service_account
from google.oauth2.service_account import Credentials
from pathlib import Path

class Config:
    """Access the configs in config.ini through this class.
    Also reads the service_account.json in the config folder. 

    Raises:
        Exception: config.ini not found
        Exception: service_account.json not found
    """

    project_id: str
    database: str
    connection: Credentials
    entities: list[str]
    output_folder: str

    @classmethod
    def initialize(cls, config_file_path: str):
        """Sets the members of the class

        Args:
            config_file_path (str): path to config.ini file. 
        """
        conf = cls.read_conf(config_file_path)
        cls.project_id = conf.get('mimiciv', 'project_id')
        cls.database = conf.get('mimiciv', 'database')
        cls.connection = cls.__get_gbq_connection()

        extractor_config = cls.__read_extractor_config()
        cls.entities = extractor_config['entities']
        cls.output_folder = extractor_config['output_folder']

    @staticmethod
    def read_conf(file_path: str) -> configparser.ConfigParser:
        """Reads and returns the config.ini file as a ConfigParser object.

        Args:
            file_path (str): path to config file.

        Raises:
            Exception: If config file not found

        Returns:
            configparser.ConfigParser: config file as object
        """
        conf = configparser.ConfigParser()
        read_count = conf.read(file_path)
        if len(read_count) == 0:
            raise Exception(f"Could not read dataset module config.ini file. Path: {file_path}")
        else:
            return conf

    @staticmethod
    def __get_gbq_connection() -> Credentials:
        """Creates a connection to the google big query project.

        Returns:
            Credentials: connection credentials to GBQ
        """
        return service_account.Credentials.from_service_account_file(
            Path(__file__).parent.joinpath('service_account.json').resolve()
        )

    @staticmethod
    def __read_extractor_config() -> dict:
        config_json = None
        json_config_path = Path(__file__).parent / 'extractor_config.json'
        with open(json_config_path.resolve()) as fp:  
            config_json = json.load(fp)
        
        return config_json


# config.ini should be in config folder
Config.initialize(str(Path(__file__).parent / 'config.ini'))