from enum import Enum


class RoomType(str, Enum):
    LIVING_ROOM = "living_room"
    BEDROOM = "bedroom"
    DINING_ROOM = "dining_room"
    HOME_OFFICE = "home_office"
    KITCHEN = "kitchen"
    BATHROOM = "bathroom"
    CHILDREN_ROOM = "children_room"
    GUEST_ROOM = "guest_room"
    GAMING_ROOM = "gaming_room"
    FITNESS_ROOM = "fitness_room"
    HOBBY_ROOM = "hobby_room"
    OTHER = "other"


class RoomShape(str, Enum):
    RECTANGLE = "rectangle"
    SQUARE = "square"
    L_SHAPE = "l_shape"
    U_SHAPE = "u_shape"
    OPEN_PLAN = "open_plan"
    IRREGULAR = "irregular"
    OTHER = "other"


class RoomLayoutType(str, Enum):
    CLOSED = "closed"
    OPEN_SPACE = "open_space"
    WALK_THROUGH = "walk_through"
    SEMI_OPEN = "semi_open"
    STUDIO = "studio"
    SPLIT_LEVEL = "split_level"
    LOFT = "loft"
    OTHER = "other"


class RoomStatus(str, Enum):
    VALIDATED = "validated"
    UNDER_REVIEW = "under_review"


class VerificationStatus(str, Enum):
    AI_DETECTED = "AI_DETECTED"
    USER_VERIFIED = "USER_VERIFIED"
    USER_CORRECTED = "USER_CORRECTED"


class ImageRole(str, Enum):
    WALL = "wall"
    OVERVIEW = "overview"
    FLOOR = "floor"
    CEILING = "ceiling"
    DETAIL = "detail"


class BuildingElementType(str, Enum):
    RADIATOR = "radiator"
    FIREPLACE = "fireplace"
    COLUMN = "column"
    STAIR = "stair"
    ROOF_SLOPE = "roof_slope"
    NICHE = "niche"
    BUILT_IN_CABINET = "built_in_cabinet"
    OTHER = "other"


class ObjectCategory(str, Enum):
    SOFA = "sofa"
    TABLE = "table"
    CHAIR = "chair"
    BED = "bed"
    CABINET = "cabinet"
    SHELF = "shelf"
    DESK = "desk"
    TELEVISION = "television"
    MONITOR = "monitor"
    LIGHTING = "lighting"
    PLANT = "plant"
    DECORATION = "decoration"
    OTHER = "other"
