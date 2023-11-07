from enum import Enum, auto


class EntityType(Enum):

    PATIENT = auto()
    MEDICATION = auto()
    ADMISSION = auto()
    DIAGNOSIS = auto()
    LABEVENT = auto()

    def __str__(self):
        return self.name

    def __repr__(self) -> str:
        return str(self)
