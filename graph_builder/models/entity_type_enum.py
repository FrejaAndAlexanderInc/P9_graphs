from enum import Enum, auto


class EntityType(Enum):

    PATIENTS = 'P'
    MEDICATION = 'M'
    ADMISSIONS = 'A'
    DIAGNOSIS = 'D'
    LABEVENTS = 'L'
    PROCEDURES = 'PR'

    def __str__(self):
        return self.name

    def __repr__(self) -> str:
        return f"{self.name}: {self.value}"

    @property
    def alias(self) -> str:
        return self.value

    @staticmethod
    def from_str(str: str):
        return EntityType[str.upper()]
