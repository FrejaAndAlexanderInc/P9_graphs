from graph_builder.config.Config import Config
from MimicDataExtractor import MimicDataExtractor

CONFIG_FILEPATH = 'config.ini' 

def main():
    config = Config(CONFIG_FILEPATH)
    mde = MimicDataExtractor(config)
    df = mde.extract_entities()
    print(df.head())

if __name__ == '__main__':
    main()