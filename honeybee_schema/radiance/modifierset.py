"""ModifierSet Schema"""
from pydantic import Field, constr
from typing import List, Union

from .._base import NoExtraBaseModel
from ._base import IDdRadianceBaseModel
from .modifier import Plastic, Glass, BSDF, Glow, Light, Trans

# Unioned Modifier Schema objects defined for type reference
_REFERENCE_UNION_MODIFIERS = Union[Plastic, Glass, BSDF, Glow, Light, Trans]


class BaseModifierSetAbridged(NoExtraBaseModel):
    """Base class for the abridged modfier sets assigned to Faces."""

    exterior_modifier: str = Field(
            default=None,
            description='Identifier for a radiance modifier object for faces with an '
                        ' Outdoors boundary condition.'
        )

    interior_modifier: str = Field(
            default=None,
            description='Identifier for a radiance modifier object for faces with a '
                        'boundary condition other than Outdoors.'
        )


class WallModifierSetAbridged(BaseModifierSetAbridged):
    """Abridged set containing radiance modifiers needed for a model's Walls."""

    type: constr(regex='^WallModifierSetAbridged$') = 'WallModifierSetAbridged'


class FloorModifierSetAbridged(BaseModifierSetAbridged):
    """Abridged set containing radiance modifiers needed for a model's Floors."""

    type: constr(regex='^FloorModifierSetAbridged$') = 'FloorModifierSetAbridged'


class RoofCeilingModifierSetAbridged(BaseModifierSetAbridged):
    """Abridged set containing radiance modifiers needed for a model's Roofs."""

    type: constr(regex='^RoofCeilingModifierSetAbridged$') = \
        'RoofCeilingModifierSetAbridged'


class ShadeModifierSetAbridged(BaseModifierSetAbridged):
    """Abridged set containing radiance modifiers needed for a model's Shade."""

    type: constr(regex='^ShadeModifierSetAbridged$') = 'ShadeModifierSetAbridged'


class ApertureModifierSetAbridged(NoExtraBaseModel):
    """Abridged set containing radiance modifiers needed for a model's Apertures."""

    type: constr(regex='^ApertureModifierSetAbridged$') = 'ApertureModifierSetAbridged'

    window_modifier: str = Field(
            default=None,
            description='Identifier of modifier object for apertures with an Outdoors '
                        'boundary condition, False is_operable property, '
                        'and Wall parent Face.'
        )

    interior_modifier: str = Field(
            default=None,
            description='Identifier of modifier object for apertures with a Surface '
                        'boundary condition.'
        )

    skylight_modifier: str = Field(
            default=None,
            description='Identifier of modifier object for apertures with an Outdoors '
                        'boundary condition, False is_operable property, and a '
                        'RoofCeiling or Floor face type for their parent face.'
        )

    operable_modifier: str = Field(
            default=None,
            description='Identifier of modifier object for apertures with an Outdoors '
                        'boundary condition and a True is_operable property.'
        )


class DoorModifierSetAbridged(BaseModifierSetAbridged):
    """Abridged set containing radiance modifiers needed for a model's Doors."""

    type: constr(regex='^DoorModifierSetAbridged$') = 'DoorModifierSetAbridged'

    exterior_modifier: str = Field(
            default=None,
            description='Identifier of modifier object for doors with an Outdoors '
                        'boundary condition.'
        )

    interior_glass_modifier: str = Field(
            default=None,
            description='Identifier of modifier object for glass with a Surface '
                        'boundary condition.'
        )

    overhead_modifier: str = Field(
            default=None,
            description='Identifier of window modifier object for doors with an '
                        'Outdoors boundary condition and a RoofCeiling or Floor '
                        'face type for their parent face.'
        )


class ModifierSetAbridged(IDdRadianceBaseModel):
    """Abridged set containing all modifiers needed to create a radiance model."""

    type: constr(regex='^ModifierSetAbridged$') = 'ModifierSetAbridged'

    wall_set: str = Field(
        default=None,
        description='Identifer for optional WallModifierSet object for this '
                    'ModifierSet (default: None).'
    )

    floor_set: str = Field(
        default=None,
        description='Identifier for optional FloorModifierSet object for '
                    'this ModifierSet (default: None).'
    )

    roof_ceiling_set: str = Field(
        default=None,
        description='Identifier for optional RoofCeilingModifierSet object for this '
                    'ModifierSet (default: None).'
    )

    aperture_set: str = Field(
        default=None,
        description='Identifier for optional ApertureModifierSet object for this '
                    'ModifierSet (default: None).'
    )

    door_set: str = Field(
        default=None,
        description='Identifier for optional DoorModifierSet object for this '
                    'ModifierSet (default: None).'
    )

    shade_set: str = Field(
        default=None,
        description='Identifier for optional ShadeModifierSet object for this '
                    'ModifierSet (default: None).'
    )

    air_boundary_modifier: str = Field(
        default=None,
        description='Identifier for optional Modifier to be used for all Faces '
                    'with an AirBoundary face type. If None, it will be the '
                    'honyebee generic air wall modifier.'
    )


class BaseModifierSet(NoExtraBaseModel):
    """Base class for the modifier sets assigned to Faces."""

    exterior_modifier: _REFERENCE_UNION_MODIFIERS = Field(
            default=None,
            description='A radiance modifier object for faces with an Outdoors boundary '
                        'condition.'
        )

    interior_modifier: _REFERENCE_UNION_MODIFIERS = Field(
            default=None,
            description='A radiance modifier object for faces with a boundary condition '
                        'other than Outdoors.'
        )


class WallModifierSet(BaseModifierSet):
    """Set containing radiance modifiers needed for a model's Walls."""

    type: constr(regex='^WallModifierSet$') = 'WallModifierSet'


class FloorModifierSet(BaseModifierSet):
    """Set containing radiance modifiers needed for a model's Floors."""

    type: constr(regex='^FloorModifierSet$') = 'FloorModifierSet'


class RoofCeilingModifierSet(BaseModifierSet):
    """Set containing radiance modifiers needed for a model's roofs."""

    type: constr(regex='^RoofCeilingModifierSet$') = 'RoofCeilingModifierSet'


class ShadeModifierSet(BaseModifierSet):
    """Set containing radiance modifiers needed for a model's Shade."""

    type: constr(regex='^ShadeModifierSet$') = 'ShadeModifierSet'


class ApertureModifierSet(NoExtraBaseModel):
    """Set containing radiance modifiers needed for a model's Apertures."""

    type: constr(regex='^ApertureModifierSet$') = 'ApertureModifierSet'

    window_modifier: _REFERENCE_UNION_MODIFIERS = Field(
            default=None,
            description='A modifier object for apertures with an Outdoors '
                        'boundary condition, False is_operable property, '
                        'and Wall parent Face.'
        )

    interior_modifier: _REFERENCE_UNION_MODIFIERS = Field(
            default=None,
            description='A modifier object for apertures with a Surface '
                        'boundary condition.'
        )

    skylight_modifier: _REFERENCE_UNION_MODIFIERS = Field(
            default=None,
            description='A modifier object for apertures with an Outdoors '
                        'boundary condition, False is_operable property, and a '
                        'RoofCeiling or Floor face type for their parent face.'
        )

    operable_modifier: _REFERENCE_UNION_MODIFIERS = Field(
            default=None,
            description='A modifier object for apertures with an Outdoors boundary '
                        'condition and a True is_operable property.'
        )


class DoorModifierSet(BaseModifierSet):
    """Set containing radiance modifiers needed for a model's Doors."""

    type: constr(regex='^DoorModifierSet$') = 'DoorModifierSet'

    exterior_modifier: _REFERENCE_UNION_MODIFIERS = Field(
            default=None,
            description='A modifier object for doors with an Outdoors '
                        'boundary condition.'
        )

    interior_glass_modifier: _REFERENCE_UNION_MODIFIERS = Field(
            default=None,
            description='A modifier object for glass with a Surface '
                        'boundary condition.'
        )

    overhead_modifier: _REFERENCE_UNION_MODIFIERS = Field(
            default=None,
            description='A window modifier object for doors with an Outdoors boundary '
                        'condition and a RoofCeiling or Floor face type for their '
                        'parent face.'
        )


class ModifierSet(IDdRadianceBaseModel):
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

    air_boundary_modifier: _REFERENCE_UNION_MODIFIERS = Field(
        default=None,
        description='An optional Modifier to be used for all Faces with an AirBoundary '
                    'face type. If None, it will be the honyebee generic air wall '
                    'modifier.'
    )


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