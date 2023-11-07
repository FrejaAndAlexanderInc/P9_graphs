from data_extractor.sepsis_extractor import SepsisDataExtractor
from graph_builder.graph_constructor.graph_constructor import GraphConstructor
from graph_builder.model_constructor import ModelConstructor

EXTRACT = False

def main():
    if EXTRACT:
        sde = SepsisDataExtractor(200, 1000, 50)
        sde.extract_all()
    mc = ModelConstructor()
    mc.build()
    breakpoint()

if __name__ == "__main__":
    main()
