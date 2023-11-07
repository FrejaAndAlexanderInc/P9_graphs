from __future__ import annotations
from graph_builder.models.entity_type_enum import EntityType
import pandas as pd


class Entity:
    """Represents all samples of an entity.
    ex. all patients.
    """

    def __init__(self, name: str, alias: str):
        self.name = name
        self.alias = alias
        self.ids = set()
        self.maps = dict()
        self.filter = dict()
        self.feat_map = dict()

    def populate(self, df: pd.DataFrame):
        self.ids = set(df[self.name].unique())

    def combine_entity(self, other_entity: Entity) -> None:
        if self.name != other_entity.name:
            raise Exception(
                f"Can't combine entities of different kinds.\nThis: {self.name}\nOther: {other_entity.name}"
            )
        self.ids = self.ids.union(other_entity.ids)

    def reindex(self, new_ids: set):
        # Save only the ids being used in relations
        self.ids = new_ids.intersection(self.ids)

        # Re-index the remaining ids and add to map
        reindex_origin_map = {new_id: old_id for new_id, old_id in enumerate(self.ids)}
        origin_reindex_map = {
            old_id: new_id for new_id, old_id in reindex_origin_map.items()
        }

        # Add maps to class for backwards compatability
        self.maps["origin-reindex"] = origin_reindex_map
        self.maps["reindex-origin"] = reindex_origin_map

        # Map ids to re-indexed ids
        self.ids = set([self.maps["origin-reindex"][id] for id in self.ids])
