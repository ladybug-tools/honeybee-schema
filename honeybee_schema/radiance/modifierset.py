"""ModifierSet Schema"""
from pydantic import Field
from typing import Union, Literal
from .._base import NoExtraBaseModel
from ._base import IDdRadianceBaseModel
from .modifier import Plastic, Glass, BSDF, Glow, Light, Trans, Metal, Void, Mirror


class BaseModifierSetAbridged(NoExtraBaseModel):
    """Base class for the abridged modifier sets assigned to Faces."""

    exterior_modifier: Union[str, None] = Field(
        default=None,
        description='Identifier for a radiance modifier object for faces with an '
                    ' Outdoors boundary condition.'
    )

    interior_modifier: Union[str, None] = Field(
        default=None,
        description='Identifier for a radiance modifier object for faces with a '
                    'boundary condition other than Outdoors.'
    )


class WallModifierSetAbridged(BaseModifierSetAbridged):
    """Abridged set containing radiance modifiers needed for a model's Walls."""

    type: Literal['WallModifierSetAbridged'] = 'WallModifierSetAbridged'


class FloorModifierSetAbridged(BaseModifierSetAbridged):
    """Abridged set containing radiance modifiers needed for a model's Floors."""

    type: Literal['FloorModifierSetAbridged'] = 'FloorModifierSetAbridged'


class RoofCeilingModifierSetAbridged(BaseModifierSetAbridged):
    """Abridged set containing radiance modifiers needed for a model's Roofs."""

    type: Literal['RoofCeilingModifierSetAbridged'] = 'RoofCeilingModifierSetAbridged'


class ShadeModifierSetAbridged(BaseModifierSetAbridged):
    """Abridged set containing radiance modifiers needed for a model's Shade."""

    type: Literal['ShadeModifierSetAbridged'] = 'ShadeModifierSetAbridged'


class ApertureModifierSetAbridged(NoExtraBaseModel):
    """Abridged set containing radiance modifiers needed for a model's Apertures."""

    type: Literal['ApertureModifierSetAbridged'] = 'ApertureModifierSetAbridged'

    window_modifier: Union[str, None] = Field(  # type: ignore
        default=None,
        description='Identifier of modifier object for apertures with an Outdoors '
                    'boundary condition, False is_operable property, '
                    'and Wall parent Face.'
    )

    interior_modifier: Union[str, None] = Field(
        default=None,
        description='Identifier of modifier object for apertures with a Surface '
                    'boundary condition.'
    )

    skylight_modifier: Union[str, None] = Field(
        default=None,
        description='Identifier of modifier object for apertures with an Outdoors '
                    'boundary condition, False is_operable property, and a '
                    'RoofCeiling or Floor face type for their parent face.'
    )

    operable_modifier: Union[str, None] = Field(
        default=None,
        description='Identifier of modifier object for apertures with an Outdoors '
                    'boundary condition and a True is_operable property.'
    )


class DoorModifierSetAbridged(BaseModifierSetAbridged):
    """Abridged set containing radiance modifiers needed for a model's Doors."""

    type: Literal['DoorModifierSetAbridged'] = 'DoorModifierSetAbridged'

    interior_glass_modifier: Union[str, None] = Field(
        default=None,
        description='Identifier of modifier object for glass with a Surface '
                    'boundary condition.'
    )

    exterior_glass_modifier: Union[str, None] = Field(
        default=None,
        description='Identifier of modifier object for glass with an Outdoors '
                    'boundary condition.'
    )

    overhead_modifier: Union[str, None] = Field(
        default=None,
        description='Identifier of a modifier object for doors with an '
                    'Outdoors boundary condition and a RoofCeiling or Floor '
                    'face type for their parent face.'
    )


class ModifierSetAbridged(IDdRadianceBaseModel):
    """Abridged set containing all modifiers needed to create a radiance model."""

    type: Literal['ModifierSetAbridged'] = 'ModifierSetAbridged'

    wall_set: Union[WallModifierSetAbridged, None] = Field(
        default=None,
        description='Optional WallModifierSet object for this '
                    'ModifierSet (default: None).'
    )

    floor_set: Union[FloorModifierSetAbridged, None] = Field(
        default=None,
        description='Optional FloorModifierSet object for '
                    'this ModifierSet (default: None).'
    )

    roof_ceiling_set: Union[RoofCeilingModifierSetAbridged, None] = Field(
        default=None,
        description='Optional RoofCeilingModifierSet object for this '
                    'ModifierSet (default: None).'
    )

    aperture_set: Union[ApertureModifierSetAbridged, None] = Field(
        default=None,
        description='Optional ApertureModifierSet object for this '
                    'ModifierSet (default: None).'
    )

    door_set: Union[DoorModifierSetAbridged, None] = Field(
        default=None,
        description='Optional DoorModifierSet object for this '
                    'ModifierSet (default: None).'
    )

    shade_set: Union[ShadeModifierSetAbridged, None] = Field(
        default=None,
        description='Optional ShadeModifierSet object for this '
                    'ModifierSet (default: None).'
    )

    air_boundary_modifier: Union[str, None] = Field(
        default=None,
        description='Optional Modifier to be used for all Faces '
                    'with an AirBoundary face type. If None, it will be the '
                    'honeybee generic air wall modifier.'
    )


class BaseModifierSet(NoExtraBaseModel):
    """Base class for the modifier sets assigned to Faces."""

    exterior_modifier: Union[Plastic, Glass, BSDF, Glow, Light, Trans, Metal, Void, Mirror, None] = Field(
        default=None,
        description='A radiance modifier object for faces with an Outdoors boundary '
                    'condition.'
    )

    interior_modifier: Union[Plastic, Glass, BSDF, Glow, Light, Trans, Metal, Void, Mirror, None] = Field(
        default=None,
        description='A radiance modifier object for faces with a boundary condition '
                    'other than Outdoors.'
    )


class WallModifierSet(BaseModifierSet):
    """Set containing radiance modifiers needed for a model's Walls."""

    type: Literal['WallModifierSet'] = 'WallModifierSet'


class FloorModifierSet(BaseModifierSet):
    """Set containing radiance modifiers needed for a model's Floors."""

    type: Literal['FloorModifierSet'] = 'FloorModifierSet'


class RoofCeilingModifierSet(BaseModifierSet):
    """Set containing radiance modifiers needed for a model's roofs."""

    type: Literal['RoofCeilingModifierSet'] = 'RoofCeilingModifierSet'


class ShadeModifierSet(BaseModifierSet):
    """Set containing radiance modifiers needed for a model's Shade."""

    type: Literal['ShadeModifierSet'] = 'ShadeModifierSet'


class ApertureModifierSet(NoExtraBaseModel):
    """Set containing radiance modifiers needed for a model's Apertures."""

    type: Literal['ApertureModifierSet'] = 'ApertureModifierSet'

    window_modifier: Union[Plastic, Glass, BSDF, Glow, Light, Trans, Metal, Void, Mirror, None] = Field(
        default=None,
        description='A modifier object for apertures with an Outdoors '
                    'boundary condition, False is_operable property, '
                    'and Wall parent Face.'
    )

    interior_modifier: Union[Plastic, Glass, BSDF, Glow, Light, Trans, Metal, Void, Mirror, None] = Field(
        default=None,
        description='A modifier object for apertures with a Surface '
                    'boundary condition.'
    )

    skylight_modifier: Union[Plastic, Glass, BSDF, Glow, Light, Trans, Metal, Void, Mirror, None] = Field(
        default=None,
        description='A modifier object for apertures with an Outdoors '
                    'boundary condition, False is_operable property, and a '
                    'RoofCeiling or Floor face type for their parent face.'
    )

    operable_modifier: Union[Plastic, Glass, BSDF, Glow, Light, Trans, Metal, Void, Mirror, None] = Field(
        default=None,
        description='A modifier object for apertures with an Outdoors boundary '
                    'condition and a True is_operable property.'
    )


class DoorModifierSet(BaseModifierSet):
    """Set containing radiance modifiers needed for a model's Doors."""

    type: Literal['DoorModifierSet'] = 'DoorModifierSet'

    interior_glass_modifier: Union[Plastic, Glass, BSDF, Glow, Light, Trans, Metal, Void, Mirror, None] = Field(
        default=None,
        description='A modifier object for glass with a Surface boundary condition.'
    )

    exterior_glass_modifier: Union[Plastic, Glass, BSDF, Glow, Light, Trans, Metal, Void, Mirror, None] = Field(
        default=None,
        description='A modifier object for glass with an Outdoors boundary condition.'
    )

    overhead_modifier: Union[Plastic, Glass, BSDF, Glow, Light, Trans, Metal, Void, Mirror, None] = Field(
        default=None,
        description='A window modifier object for doors with an Outdoors boundary '
                    'condition and a RoofCeiling or Floor face type for their '
                    'parent face.'
    )


class ModifierSet(IDdRadianceBaseModel):
    """Set containing all radiance modifiers needed to create a radiance model."""

    type: Literal['ModifierSet'] = 'ModifierSet'

    wall_set: Union[WallModifierSet, None] = Field(
        default=None,
        description='An optional WallModifierSet object for this ModifierSet. '
                    '(default: None).'
    )

    floor_set: Union[FloorModifierSet, None] = Field(
        default=None,
        description='An optional FloorModifierSet object for this ModifierSet. '
                    '(default: None).'
    )

    roof_ceiling_set: Union[RoofCeilingModifierSet, None] = Field(
        default=None,
        description='An optional RoofCeilingModifierSet object for this ModifierSet. '
                    '(default: None).'
    )

    aperture_set: Union[ApertureModifierSet, None] = Field(
        default=None,
        description='An optional ApertureModifierSet object for this ModifierSet. '
                    '(default: None).'
    )

    door_set: Union[DoorModifierSet, None] = Field(
        default=None,
        description='An optional DoorModifierSet object for this ModifierSet. '
                    '(default: None).'
    )

    shade_set: Union[ShadeModifierSet, None] = Field(
        default=None,
        description='An optional ShadeModifierSet object for this ModifierSet. '
                    '(default: None).'
    )

    air_boundary_modifier: Union[Plastic, Glass, BSDF, Glow, Light, Trans, Metal, Void, Mirror, None] = Field(
        default=None,
        description='An optional Modifier to be used for all Faces with an AirBoundary '
                    'face type. If None, it will be the honeybee generic air wall '
                    'modifier.'
    )
