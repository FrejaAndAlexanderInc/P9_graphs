import configparser
import json
from google.oauth2 import service_account
from google.oauth2.service_account import Credentials
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / 'config.ini'
EXTRACTOR_CONFIG_PATH = Path(__file__).parent / 'extractor_config.json'

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
    relations: list[dict]
    output_folder: str

    @classmethod
    def initialize(cls, config_file_path: str, extractor_config_path: str):
        """Sets the members of the class

        Args:
            config_file_path (str): path to config.ini file. 
            extractor_config_path (str): path to extractor config file.
        """
        conf = cls.read_conf(config_file_path)
        cls.project_id = conf.get('mimiciv', 'project_id')
        cls.connection = cls.__get_gbq_connection()

        extractor_config = cls.__read_extractor_config(extractor_config_path)
        cls.entities = extractor_config['entities']
        cls.relations = extractor_config['relations']
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
    def __read_extractor_config(config_path: str) -> dict:
        config_json = None
        with open(config_path) as fp:  
            config_json = json.load(fp)
        
        return config_json


Config.initialize(str(CONFIG_PATH), str(EXTRACTOR_CONFIG_PATH))
