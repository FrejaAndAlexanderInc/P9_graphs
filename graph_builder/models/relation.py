from pandas import DataFrame
import torch as th
from graph_builder.models.entity import Entity
from enum import Enum, auto

class Direction(Enum):
    forward = auto()
    backward = auto()
    bidirectional = auto()
    none = () 

    def direction_names(self) -> list[str]:
        return [d.name for d in Direction]

class Relation:
    def __init__(
        self,
        sub: Entity,
        obj: Entity,
        relation_name: str,
        mapping: DataFrame,
        aux: bool = False,
    ):
        self.relation_name = relation_name
        self.direction = Direction.bidirectional
        self.aux = aux
        self.sub = sub
        self.obj = obj
        self.mapping = self.construct_mapping(mapping)

    def construct_mapping(self, mapping: DataFrame) -> DataFrame:
        # Filter mappings with non-existing entity ids
        mapping = mapping[mapping[self.sub.name].isin(self.sub.ids)]
        mapping = mapping[mapping[self.obj.name].isin(self.obj.ids)]

        # Drop duplicate rows
        mapping.drop_duplicates(inplace=True)

        return mapping

    def set_direction(self, direction: Direction):
        self.direction = direction

    def construct_graph_relations(self):
        relations_dict = dict()

        # Extract subject and object values from mapping
        sub_values = self.mapping[self.sub.name].values
        obj_values = self.mapping[self.obj.name].values

        # Convert to tensors
        subject_tensor = th.tensor(sub_values, dtype=th.int64)
        object_tensor = th.tensor(obj_values, dtype=th.int64)

        # Get entity aliases
        sub_alias = self.sub.alias
        obj_alias = self.obj.alias
        rel_name = self.relation_name
        rel_name_reverse = rel_name[::-1]

        # Create relations based on directionality
        if self.direction == Direction.forward:
            relations_dict[(sub_alias, rel_name, obj_alias)] = (
                subject_tensor,
                object_tensor,
            )
        elif self.direction == Direction.backward:
            relations_dict[(obj_alias, rel_name_reverse, sub_alias)] = (
                object_tensor,
                subject_tensor,
            )
        elif self.direction == Direction.bidirectional:
            relations_dict[(sub_alias, rel_name, obj_alias)] = (
                subject_tensor,
                object_tensor,
            )
            relations_dict[(obj_alias, rel_name_reverse, sub_alias)] = (
                object_tensor,
                subject_tensor,
            )

        print(
            f"Constructed {self.direction} relation {rel_name} between "
            f"{len(set(sub_values))} {sub_alias} and {len(set(obj_values))} {obj_alias}"
        )

        return relations_dict
