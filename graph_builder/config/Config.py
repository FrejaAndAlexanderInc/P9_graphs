import configparser

class Config:
    def __init__(self, file_path: str) -> None:
        conf = configparser.ConfigParser()

        try:
            conf.read(file_path)
        except:
            print("Could not read dataset module config.ini file")

        self.project_id = conf.get('mimiciv', 'project_id')
        self.database = conf.get('mimiciv', 'database')
        self.credentials = 'service_account.json'