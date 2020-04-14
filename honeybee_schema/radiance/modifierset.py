"""ModifierSet Schema"""
from pydantic import Field, constr
from typing import List, Union

from .._base import IDdBaseModel
from .modifier import ModifierBase, Void


class BaseModifierSet(IDdBaseModel):
    """Base class for the sets assigned to Faces."""

    # TODO: What to use for default? Void or None?
    exterior_modifier: ModifierBase = Field(
            default=Void(),
            description='A radiance modifier object for faces with an Outdoors boundary '
                        'condition.'
        )
    # TODO: What to use for default? Void or None?
    interior_modifier: ModifierBase = Field(
            default=Void(),
            description='A radiance modifier object for faces with a boundary condition '
                        'other than Outdoors.'
        )


class WallModifierSet(BaseModifierSet):
    """Set containing all radiance modifiers needed to for a radiance model's Walls."""

    type: constr(regex='^WallModifierSet$') = 'WallModifierSet'


class FloorModifierSet(BaseModifierSet):
    """Set containing all radiance modifiers needed to for a radiance model's Floors."""

    type: constr(regex='^FloorModifierSet$') = 'FloorModifierSet'


class RoofCeilingModifierSet(BaseModifierSet):
    """Set containing all radiance modifiers needed to for a radiance model's roofs."""

    type: constr(regex='^RoofCeilingModifierSet$') = 'RoofCeilingModifierSet'


class ShadeModifierSet(BaseModifierSet):
    """Set containing all radiance modifiers needed to for a radiance model's Shade."""

    type: constr(regex='^ShadeModifierSet$') = 'ShadeModifierSet'


class ApertureModifierSet(BaseModifierSet):
    """Set containing all radiance modifiers needed to for a radiance model's Apertures."""

    type: constr(regex='^ApertureModifierSet$') = 'ApertureModifierSet'

    window_modifier: ModifierBase = Field(
            default=Void(),
            description='A modifier object for apertures with an Outdoors '
                        'boundary condition, False is_operable property, '
                        'and Wall parent Face.'
        )

    interior_modifier: ModifierBase = Field(
            default=Void(),
            description='A modifier object for apertures with a Surface '
                        'boundary condition.'
        )

    skylight_modifier: ModifierBase = Field(
            default=Void(),
            description='A modifier object for apertures with an Outdoors '
                        'boundary condition, False is_operable property, and a '
                        'RoofCeiling or Floor face type for their parent face.'
        )

    operable_modifier: ModifierBase = Field(
            default=Void(),
            description='A modifier object for apertures with an Outdoors boundary '
                        'condition and a True is_operable property.'
        )


class DoorModifierSet(BaseModifierSet):
    """Set containing all radiance modifiers needed to for a radiance model's Doors."""

    type: constr(regex='^DoorModifierSet$') = 'DoorModifierSet'

    exterior_modifier: ModifierBase = Field(
            default=Void(),
            description='A modifier object for doors with an Outdoors '
                        'boundary condition.'
        )

    interior_modifier: ModifierBase = Field(
            default=Void(),
            description='A modifier object for doors with a Surface '
                        'boundary condition.'
        )

    exterior_glass_modifier: ModifierBase = Field(
            default=Void(),
            description='A modifier object for glass with an Outdoors '
                        'boundary condition.'
        )

    interior_glass_modifier: ModifierBase = Field(
            default=Void(),
            description='A modifier object for glass with a Surface '
                        'boundary condition.'
        )

    overhead_modifier: ModifierBase = Field(
            default=Void(),
            description='A window modifier object for doors with an Outdoors boundary '
                        'condition and a RoofCeiling or Floor face type for their '
                        'parent face.'
        )


class ModifierSet(IDdBaseModel):
    """Set containing all radiance modifiers needed to create a radiance model."""

    type: constr(regex='^ModifierSet$') = 'ModifierSet'

    wall_set: WallModifierSet = Field(
        default=None,
        description='An optional WallModifierSet object for this ModifierSet. '
                    '(default: None).'
    )

    floor_set: FloorModifierSet = Field(
        default=None,
        description='An optional FloorModifierSet object for this ModifierSet. '
                    '(default: None).'
    )

    roof_ceiling_set: RoofCeilingModifierSet = Field(
        default=None,
        description='An optional RoofCeilingModifierSet object for this ModifierSet. '
                    '(default: None).'
    )

    aperture_set: ApertureModifierSet = Field(
        default=None,
        description='An optional ApertureModifierSet object for this ModifierSet. '
                    '(default: None).'
    )

    door_set: DoorModifierSet = Field(
        default=None,
        description='An optional DoorModifierSet object for this ModifierSet. '
                    '(default: None).'
    )

    shade_set: ShadeModifierSet = Field(
        default=None,
        description='An optional ShadeModifierSet object for this ModifierSet. '
                    '(default: None).'
    )

    # TODO: This requires default modfiers from honeybee-radiance? How to schematize?
    # air_boundary_modifier: AirWallModifier = Field(...)


# TODO: for testing will delete after PR accepted.
if __name__ == "__main__":
    print(BaseModifierSet.schema_json(indent=2))
    print(WallModifierSet.schema_json(indent=2))
    print(FloorModifierSet.schema_json(indent=2))
    print(RoofCeilingModifierSet.schema_json(indent=2))
    print(ShadeModifierSet.schema_json(indent=2))
    print(ApertureModifierSet.schema_json(indent=2))
    print(DoorModifierSet.schema_json(indent=2))
    print(ModifierSet.schema_json(indent=2))