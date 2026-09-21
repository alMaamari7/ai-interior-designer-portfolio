from enum import Enum


class DesiredAtmosphere(str, Enum):
    COZY = "cozy"
    CALM = "calm"
    SERENE = "serene"
    INVITING = "inviting"
    MODERN = "modern"
    MINIMALIST = "minimalist"
    NATURAL = "natural"
    ELEGANT = "elegant"
    LUXURIOUS = "luxurious"
    PLAYFUL = "playful"
    CREATIVE = "creative"
    BRIGHT = "bright"
    SOPHISTICATED = "sophisticated"
    INDUSTRIAL = "industrial"


class ModifiableArea(str, Enum):
    FURNITURE = "furniture"
    DECORATION = "decoration"
    TEXTILES = "textiles"
    LIGHTING = "lighting"
    PLANTS = "plants"
    WALL_COLORS = "wall_colors"
    FLOORING = "flooring"
    WINDOW_TREATMENTS = "window_treatments"
    BUILDING_ELEMENTS = "building_elements"
    ROOM_LAYOUT = "room_layout"


class OwnershipType(str, Enum):
    OWNER = "owner"
    RENTED = "rented"


class PropertyUsage(str, Enum):
    PRIMARY_RESIDENCE = "primary_residence"
    VACATION_HOME = "vacation_home"
    COMMERCIAL = "commercial"
