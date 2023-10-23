from pathlib import Path

from graph_builder.config.Config import Config
Config.initialize(str(Path.cwd() / 'config/config.ini'))

from MimicDataExtractor import MimicDataExtractor

def main():
    mde = MimicDataExtractor()
    df = mde.extract_entities()
    print(df.head())

if __name__ == '__main__':
    main()