from pydantic import BaseModel, ConfigDict, Field

from app.core.enums.design_request import (
    DesiredAtmosphere,
    ModifiableArea,
    OwnershipType,
    PropertyUsage,
)


class HouseholdData(BaseModel):
    adult_count: int = Field(ge=0)
    children_count: int = Field(ge=0)
    children_ages: list[int] = Field(default_factory=list)
    pet_count: int = Field(ge=0)
    pet_types: list[str] = Field(default_factory=list)


class BudgetData(BaseModel):
    minimum_budget: int = Field(ge=0)
    maximum_budget: int = Field(ge=0)
    currency: str = "EUR"


class DesignGoalData(BaseModel):
    goal_description: str
    desired_atmospheres: list[DesiredAtmosphere] = Field(default_factory=list)
    desired_brightness: int = Field(ge=1, le=10)
    desired_warmth: int = Field(ge=1, le=10)
    desired_naturalness: int = Field(ge=1, le=10)
    desired_minimalism: int = Field(ge=1, le=10)
    desired_color_intensity: int = Field(ge=1, le=10)
    preferred_styles: list[str] = Field(default_factory=list)


class ImprovementNeedData(BaseModel):
    improvement_description: str


class ConstraintData(BaseModel):
    ownership_type: OwnershipType
    property_usage: PropertyUsage
    allow_wall_mounting: bool
    modifiable_areas: list[ModifiableArea] = Field(default_factory=list)
    room_object_ids_to_keep: list[int] = Field(default_factory=list)
    additional_constraints: str | None = None


class CreateDesignRequestRequest(BaseModel):
    """User intent kept separate from the persistent current-room state."""

    design_request: str
    budget: BudgetData
    design_goal: DesignGoalData
    improvement_needs: list[ImprovementNeedData] = Field(default_factory=list)
    constraint: ConstraintData
    household: HouseholdData | None = None
    room_functions: list[str] = Field(default_factory=list)
    room_activities: list[str] = Field(default_factory=list)


class CreateDesignRequestResponse(BaseModel):
    design_request_id: int


class DesignRequestView(CreateDesignRequestRequest):
    model_config = ConfigDict(from_attributes=True)
    design_request_id: int


class UpdateDesignRequestRequest(BaseModel):
    design_request: str | None = None
    budget: BudgetData | None = None
    design_goal: DesignGoalData | None = None
    improvement_needs: list[ImprovementNeedData] | None = None
    constraint: ConstraintData | None = None
    household: HouseholdData | None = None
    room_functions: list[str] | None = None
    room_activities: list[str] | None = None
