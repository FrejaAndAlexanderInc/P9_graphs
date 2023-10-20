from graph_builder.config.Config import Config
from MimicDataExtractor import MimicDataExtractor
from pathlib import Path

CONFIG_FILEPATH = str(Path.cwd() / '/config/config.ini')

def main():
    config = Config(CONFIG_FILEPATH)
    mde = MimicDataExtractor(config)
    df = mde.extract_entities()
    print(df.head())

if __name__ == '__main__':
    main()