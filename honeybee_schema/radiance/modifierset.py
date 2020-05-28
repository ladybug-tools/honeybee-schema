"""ModifierSet Schema"""
from pydantic import Field, constr
from .._base import NoExtraBaseModel
from ._base import IDdRadianceBaseModel
from .modifier import _REFERENCE_UNION_MODIFIERS


class BaseModifierSetAbridged(NoExtraBaseModel):
    """Base class for the abridged modifier sets assigned to Faces."""

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

    interior_glass_modifier: str = Field(
        default=None,
        description='Identifier of modifier object for glass with a Surface '
                    'boundary condition.'
    )

    exterior_glass_modifier: str = Field(
        default=None,
        description='Identifier of modifier object for glass with an Outdoors '
                    'boundary condition.'
    )

    overhead_modifier: str = Field(
        default=None,
        description='Identifier of a modifier object for doors with an '
                    'Outdoors boundary condition and a RoofCeiling or Floor '
                    'face type for their parent face.'
    )


class ModifierSetAbridged(IDdRadianceBaseModel):
    """Abridged set containing all modifiers needed to create a radiance model."""

    type: constr(regex='^ModifierSetAbridged$') = 'ModifierSetAbridged'

    wall_set: WallModifierSetAbridged = Field(
        default=None,
        description='Optional WallModifierSet object for this '
                    'ModifierSet (default: None).'
    )

    floor_set: FloorModifierSetAbridged = Field(
        default=None,
        description='Optional FloorModifierSet object for '
                    'this ModifierSet (default: None).'
    )

    roof_ceiling_set: RoofCeilingModifierSetAbridged = Field(
        default=None,
        description='Optional RoofCeilingModifierSet object for this '
                    'ModifierSet (default: None).'
    )

    aperture_set: ApertureModifierSetAbridged = Field(
        default=None,
        description='Optional ApertureModifierSet object for this '
                    'ModifierSet (default: None).'
    )

    door_set: DoorModifierSetAbridged = Field(
        default=None,
        description='Optional DoorModifierSet object for this '
                    'ModifierSet (default: None).'
    )

    shade_set: ShadeModifierSetAbridged = Field(
        default=None,
        description='Optional ShadeModifierSet object for this '
                    'ModifierSet (default: None).'
    )

    air_boundary_modifier: str = Field(
        default=None,
        description='Optional Modifier to be used for all Faces '
                    'with an AirBoundary face type. If None, it will be the '
                    'honeybee generic air wall modifier.'
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

    interior_glass_modifier: _REFERENCE_UNION_MODIFIERS = Field(
        default=None,
        description='A modifier object for glass with a Surface boundary condition.'
    )

    exterior_glass_modifier: _REFERENCE_UNION_MODIFIERS = Field(
        default=None,
        description='A modifier object for glass with an Outdoors boundary condition.'
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
                    'face type. If None, it will be the honeybee generic air wall '
                    'modifier.'
    )
