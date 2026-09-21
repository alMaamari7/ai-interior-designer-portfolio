from enum import Enum


class WallType(str, Enum):
    INTERIOR = "INTERIOR"
    EXTERIOR = "EXTERIOR"
    PARTITION = "PARTITION"
    OTHER = "OTHER"


class WallUsability(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class FloorMaterial(str, Enum):
    WOOD = "WOOD"
    PARQUET = "PARQUET"
    LAMINATE = "LAMINATE"
    VINYL = "VINYL"
    PVC = "PVC"
    TILE = "TILE"
    STONE = "STONE"
    MARBLE = "MARBLE"
    GRANITE = "GRANITE"
    TERRAZZO = "TERRAZZO"
    CONCRETE = "CONCRETE"
    EPOXY = "EPOXY"
    CARPET = "CARPET"
    CORK = "CORK"
    BAMBOO = "BAMBOO"
    LINOLEUM = "LINOLEUM"
    RUBBER = "RUBBER"
    OTHER = "OTHER"
    UNKNOWN = "UNKNOWN"


class WindowType(str, Enum):
    STANDARD = "standard"
    PANORAMIC = "panoramic"
    ROOF = "roof"
    BALCONY_DOOR = "balcony_door"


class DoorType(str, Enum):
    STANDARD = "standard"
    DOUBLE = "double"


class DoorOpeningType(str, Enum):
    HINGED = "hinged"
    SLIDING = "sliding"
    FOLDING = "folding"
