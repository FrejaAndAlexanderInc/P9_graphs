from graph_builder.entities.entity_type_enum import EntityType

class Entity:
    
    # TODO: figure out types
    def __init__(self, entity_type: EntityType, features: list, label: ...) -> None:
        self.type = entity_type
        self.features = features
        self.label = label

    # TODO: not implemented
    def to_dlg_node(self):
        return ...