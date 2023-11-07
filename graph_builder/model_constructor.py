import os
from pathlib import Path
from typing import Optional, Union
import pandas as pd
from graph_builder.models.relation import Direction
from models.entity import Entity
from models.relation import Relation
from models.feature import Feature
from config.Config import Config


class ModelConstructor:
    def __init__(self) -> None:
        self.entities: dict[str, Entity] = {}
        self.relations: dict[str, Relation] = {}
        self.features: dict[str, Feature] = {}

    def build(self):
        self.construct_entities()
        self.construct_features()
        self.construct_relations()
        self.combine_patients()

    def combine_patients(self):
        patients = self.entities["patient"]
        sepsis_patients = self.entities["sepsis_cohort"]
        patients.combine_entity(sepsis_patients)

    def construct_entities(self):
        for ent in Config.entities:
            # Read entity information from conf
            name = ent["name"]
            alias = ent["alias"]

            # Create new Entity
            new_entity = Entity(name, alias)

            # Read parquet file with entity ids
            df = self.safe_read(Path(Config.output_folder) / f"{name}.parquet", name)

            # Populate the new entity with ids
            new_entity.populate(df)

            self.entities[name] = new_entity

    def construct_relations(self):
        for rel in Config.relations:
            # Read relation information
            file_name = rel["file_name"]
            relation_name = rel["relation_name"]
            direction = Direction(rel["direction"])
            sub = rel["sub"]
            obj = rel["obj"]

            entity1 = self.entities[sub]
            entity2 = self.entities[obj]

            # Read parquet file with entity ids
            df = self.safe_read(
                Path(Config.output_folder) / f"{file_name}.parquet", file_name
            )

            # Construct new Relation
            new_relation = Relation(
                sub=entity1,
                obj=entity2,
                relation_name=relation_name,
                mapping=df,
            )

            self.relations[file_name] = new_relation

    def construct_features(self):
        for rel in Config.features:
            # Read relation information
            file_name = rel["file_name"]
            relation_name = rel["relation_name"]
            direction = Direction(rel["direction"])
            sub = rel["sub"]
            obj = rel["obj"]

            entity1 = self.entities[sub]
            entity2 = self.entities[obj]

            # Read parquet file with entity ids
            df = self.safe_read(
                Path(Config.output_folder) / f"{file_name}.parquet", file_name
            )

            # Construct new Relation
            new_relation = Relation(
                sub=entity1,
                obj=entity2,
                relation_name=relation_name,
                mapping=df,
            )

            self.relations[file_name] = new_relation

    def safe_read(self, file_path: Path, name: str) -> Optional[pd.DataFrame]:
        if os.path.exists(file_path):
            return pd.read_parquet(file_path)
        else:
            exit(f"Could not find entity file {name}.parquet, did you extract it?")
