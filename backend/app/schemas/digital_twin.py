from pydantic import BaseModel, ConfigDict, Field


class FloorView(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    floor_material: str | None = None
    floor_color_name: str | None = None
    floor_color_hex: str | None = None


class WindowView(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    window_order: int
    window_type: str
    position_x_ratio: float
    width_ratio: float
    height_ratio: float
    confidence_score: float | None = None


class DoorView(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    door_order: int
    door_type: str
    door_opening_type: str
    position_x_ratio: float
    width_ratio: float
    height_ratio: float
    confidence_score: float | None = None


class WallView(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    wall_order: int
    wall_type: str | None = None
    wall_height: float | None = None
    wall_color_name: str | None = None
    wall_color_hex: str | None = None
    wall_usability: str | None = None
    is_accent_wall: bool | None = None
    windows: list[WindowView] = Field(default_factory=list)
    doors: list[DoorView] = Field(default_factory=list)
    confidence_score: float | None = None


class BuildingElementView(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    building_element_type: str
    position_x_ratio: float
    position_y_ratio: float
    width_ratio: float
    height_ratio: float
    confidence_score: float | None = None


class RoomObjectView(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    object_category: str
    object_type: str
    object_material: str | None = None
    object_color_name: str | None = None
    object_color_hex: str | None = None
    position_x_ratio: float
    position_y_ratio: float
    width_ratio: float
    depth_ratio: float
    rotation_angle: float
    confidence_score: float | None = None


class DigitalTwinDraftView(BaseModel):
    """Public application view of the structured current room state."""

    room_name: str | None = None
    status: str
    floor: FloorView | None = None
    walls: list[WallView] = Field(default_factory=list)
    building_elements: list[BuildingElementView] = Field(default_factory=list)
    room_objects: list[RoomObjectView] = Field(default_factory=list)


class UpdateFloor(BaseModel):
    floor_material: str | None = None
    floor_color_name: str | None = None
    floor_color_hex: str | None = None


class UpdateWindow(BaseModel):
    id: int
    window_type: str | None = None
    position_x_ratio: float | None = None
    width_ratio: float | None = None
    height_ratio: float | None = None


class UpdateDoor(BaseModel):
    id: int
    door_type: str | None = None
    door_opening_type: str | None = None
    position_x_ratio: float | None = None
    width_ratio: float | None = None
    height_ratio: float | None = None


class UpdateWall(BaseModel):
    id: int
    wall_type: str | None = None
    wall_height: float | None = None
    wall_color_name: str | None = None
    wall_color_hex: str | None = None
    wall_usability: str | None = None
    is_accent_wall: bool | None = None


class UpdateBuildingElement(BaseModel):
    id: int
    building_element_type: str | None = None
    position_x_ratio: float | None = None
    position_y_ratio: float | None = None
    width_ratio: float | None = None
    height_ratio: float | None = None


class UpdateRoomObject(BaseModel):
    id: int
    object_category: str | None = None
    object_type: str | None = None
    object_material: str | None = None
    object_color_name: str | None = None
    object_color_hex: str | None = None
    position_x_ratio: float | None = None
    position_y_ratio: float | None = None
    width_ratio: float | None = None
    depth_ratio: float | None = None
    rotation_angle: float | None = None


class UpdatedDigitalTwinData(BaseModel):
    floor: UpdateFloor | None = None
    walls: list[UpdateWall] = Field(default_factory=list)
    windows: list[UpdateWindow] = Field(default_factory=list)
    doors: list[UpdateDoor] = Field(default_factory=list)
    building_elements: list[UpdateBuildingElement] = Field(default_factory=list)
    room_objects: list[UpdateRoomObject] = Field(default_factory=list)


class CreateWindow(BaseModel):
    wall_id: int
    window_type: str
    position_x_ratio: float
    width_ratio: float
    height_ratio: float


class CreateDoor(BaseModel):
    wall_id: int
    door_type: str
    door_opening_type: str
    position_x_ratio: float
    width_ratio: float
    height_ratio: float


class CreateBuildingElement(BaseModel):
    building_element_type: str
    position_x_ratio: float
    position_y_ratio: float
    width_ratio: float
    height_ratio: float


class CreateRoomObject(BaseModel):
    object_category: str
    object_type: str
    object_material: str | None = None
    object_color_name: str | None = None
    object_color_hex: str | None = None
    position_x_ratio: float
    position_y_ratio: float
    width_ratio: float
    depth_ratio: float
    rotation_angle: float


class CreatedDigitalTwinData(BaseModel):
    windows: list[CreateWindow] = Field(default_factory=list)
    doors: list[CreateDoor] = Field(default_factory=list)
    building_elements: list[CreateBuildingElement] = Field(default_factory=list)
    room_objects: list[CreateRoomObject] = Field(default_factory=list)


class DeletedDigitalTwinData(BaseModel):
    window_ids: list[int] = Field(default_factory=list)
    door_ids: list[int] = Field(default_factory=list)
    building_element_ids: list[int] = Field(default_factory=list)
    room_object_ids: list[int] = Field(default_factory=list)


class UpdateDigitalTwinDraftRequest(BaseModel):
    """Human-review contract for correcting the AI-derived room state."""

    updated: UpdatedDigitalTwinData | None = None
    created: CreatedDigitalTwinData | None = None
    deleted: DeletedDigitalTwinData | None = None
