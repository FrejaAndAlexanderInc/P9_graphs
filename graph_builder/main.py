from data_extractor.sepsis_extractor import SepsisDataExtractor
from graph_builder.graph_constructor.graph_constructor import GraphConstructor
from graph_builder.model_constructor import ModelConstructor


def main():
    sde = SepsisDataExtractor(200, 1000, 50)
    sde.extract_features()
    mc = ModelConstructor()
    # mc.build()
    GraphConstructor()


if __name__ == "__main__":
    main()
