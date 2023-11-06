from pathlib import Path
from graph_builder.graph_constructor.graph_constructor import GraphConstructor
import pandas as pd 
from graph_builder.config.Config import Config
from graph_builder.models.relation import Relation

class SepsisGraphConstructor(GraphConstructor):
    def __init__(self):
        self.graph = Graph()

    def construct_relations(self):
        for rel in Config.relations:
            # Read relation information
            file_name = rel['file_name']
            relation_name = rel['relation_name']
            direction = rel['direction']
            sub = rel['sub']
            obj = rel['obj']
            entity1 = self.graph.get_entity(sub)
            entity2 = self.graph.get_entity(obj)

            # Read parquet file with entity ids
            mapping_df = pd.read_parquet(Path(Config.output_folder) / f'{file_name}.parquet')

            # Construct new Relation
            new_relation = Relation(
                sub=entity1,
                obj=entity2,
                relation_name=relation_name,
                mapping=mapping_df,
            )

            # Set directionality
            new_relation.set_direction(direction)

            # Add relation to graph
            self.graph.add_relation(new_relation)
