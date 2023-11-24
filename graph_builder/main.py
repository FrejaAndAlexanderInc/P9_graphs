from data_extractor.sepsis_extractor import SepsisDataExtractor
from graph_builder.graph_builder import GraphBuilder
from graph_builder.model_constructor import ModelConstructor

EXTRACT = False

def main():
    if EXTRACT:
        sde = SepsisDataExtractor(200, 1000, 50)
        sde.extract_all()
    mc = ModelConstructor()
    entities, relations, features = mc.build()
    g = GraphBuilder(entities, relations, features)
    dgl_graph = g.create_graph()
    breakpoint()

if __name__ == "__main__":
    main()
