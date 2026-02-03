"""ConstructionSet Schema"""
from pydantic import Field
from typing import Union, Literal

from .._base import NoExtraBaseModel
from ._base import IDdEnergyBaseModel
from .construction import OpaqueConstruction, WindowConstruction, ShadeConstruction, \
    AirBoundaryConstruction, WindowConstructionShade, WindowConstructionDynamic


class _FaceSubSetAbridged(NoExtraBaseModel):
    """A set of constructions for wall, floor, or roof assemblies."""

    interior_construction: Union[str, None] = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier for an OpaqueConstruction for faces with a Surface or '
        'Adiabatic boundary condition.'
    )

    exterior_construction: Union[str, None] = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier for an OpaqueConstruction for faces with an Outdoors '
        'boundary condition.'
    )

    ground_construction: Union[str, None] = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier for an OpaqueConstruction for faces with a Ground '
        'boundary condition.'
    )


class WallConstructionSetAbridged(_FaceSubSetAbridged):
    """A set of constructions for wall assemblies."""

    type: Literal['WallConstructionSetAbridged'] = 'WallConstructionSetAbridged'


class FloorConstructionSetAbridged(_FaceSubSetAbridged):
    """A set of constructions for floor assemblies."""

    type: Literal['FloorConstructionSetAbridged'] = 'FloorConstructionSetAbridged'


class RoofCeilingConstructionSetAbridged(_FaceSubSetAbridged):
    """A set of constructions for roof and ceiling assemblies."""

    type: Literal['RoofCeilingConstructionSetAbridged'] = 'RoofCeilingConstructionSetAbridged'


class _FaceSubSet(NoExtraBaseModel):
    """A set of constructions for wall, floor, or roof assemblies."""

    interior_construction: Union[OpaqueConstruction, None] = Field(
        default=None,
        description='An OpaqueConstruction for walls with a Surface or '
        'Adiabatic boundary condition.'
    )

    exterior_construction: Union[OpaqueConstruction, None] = Field(
        default=None,
        description='An OpaqueConstruction for walls with an Outdoors '
        'boundary condition.'
    )

    ground_construction: Union[OpaqueConstruction, None] = Field(
        default=None,
        description='An OpaqueConstruction for walls with a Ground '
        'boundary condition.'
    )


class WallConstructionSet(_FaceSubSet):
    """A set of constructions for wall assemblies."""

    type: Literal['WallConstructionSet'] = 'WallConstructionSet'


class FloorConstructionSet(_FaceSubSet):
    """A set of constructions for floor assemblies."""

    type: Literal['FloorConstructionSet'] = 'FloorConstructionSet'


class RoofCeilingConstructionSet(_FaceSubSet):
    """A set of constructions for roof and ceiling assemblies."""

    type: Literal['RoofCeilingConstructionSet'] = 'RoofCeilingConstructionSet'


class ApertureConstructionSetAbridged(NoExtraBaseModel):
    """A set of constructions for aperture assemblies."""

    type: Literal['ApertureConstructionSetAbridged'] = 'ApertureConstructionSetAbridged'

    interior_construction: Union[str, None] = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier for a WindowConstruction for all apertures with a '
        'Surface boundary condition.'
    )

    window_construction: Union[str, None] = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier for a WindowConstruction for apertures with an '
        'Outdoors boundary condition, False is_operable property, and a Wall '
        'face type for their parent face.'
    )

    skylight_construction: Union[str, None] = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier for a WindowConstruction for apertures with a Outdoors '
        'boundary condition, False is_operable property, and a RoofCeiling or '
        'Floor face type for their parent face.'
    )

    operable_construction: Union[str, None] = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier for a WindowConstruction for all apertures with an '
        'Outdoors boundary condition and True is_operable property.'
    )


class ApertureConstructionSet(NoExtraBaseModel):
    """A set of constructions for aperture assemblies."""

    type: Literal['ApertureConstructionSet'] = 'ApertureConstructionSet'

    interior_construction: Union[
        WindowConstruction, WindowConstructionShade, WindowConstructionDynamic, None
    ] = Field(
        default=None, description='A WindowConstruction for all apertures with a '
        'Surface boundary condition.'
    )

    window_construction: Union[
        WindowConstruction, WindowConstructionShade, WindowConstructionDynamic, None
    ] = Field(
        default=None, description='A WindowConstruction for apertures with an '
        'Outdoors boundary condition, False is_operable property, and a Wall '
        'face type for their parent face.'
    )

    skylight_construction: Union[
        WindowConstruction, WindowConstructionShade, WindowConstructionDynamic, None
    ] = Field(
        default=None,
        description='A WindowConstruction for apertures with a Outdoors boundary '
        'condition, False is_operable property, and a RoofCeiling or '
        'Floor face type for their parent face.'
    )

    operable_construction: Union[
        WindowConstruction, WindowConstructionShade, WindowConstructionDynamic, None
    ] = Field(
        default=None,
        description='A WindowConstruction for all apertures with an '
        'Outdoors boundary condition and True is_operable property.'
    )


class DoorConstructionSetAbridged(NoExtraBaseModel):
    """A set of constructions for door assemblies."""

    type: Literal['DoorConstructionSetAbridged'] = 'DoorConstructionSetAbridged'

    interior_construction: Union[str, None] = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier for an OpaqueConstruction for all opaque doors with a '
        'Surface boundary condition.'
    )

    exterior_construction: Union[str, None] = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier for an OpaqueConstruction for opaque doors with an '
        'Outdoors boundary condition and a Wall face type for their parent face.'
    )

    overhead_construction: Union[str, None] = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier for an OpaqueConstruction for opaque doors with an '
        'Outdoors boundary condition and a RoofCeiling or Floor type for '
        'their parent face.'
    )

    exterior_glass_construction: Union[str, None] = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier for a WindowConstruction for all glass doors with an '
        'Outdoors boundary condition.'
    )

    interior_glass_construction: Union[str, None] = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier for a WindowConstruction for all glass doors with a '
        'Surface boundary condition.'
    )


class DoorConstructionSet(NoExtraBaseModel):
    """A set of constructions for door assemblies."""

    type: Literal['DoorConstructionSet'] = 'DoorConstructionSet'

    interior_construction: Union[OpaqueConstruction, None] = Field(
        default=None,
        description='An OpaqueConstruction for all opaque doors with a '
        'Surface boundary condition.'
    )

    exterior_construction: Union[OpaqueConstruction, None] = Field(
        default=None,
        description='An OpaqueConstruction for opaque doors with an '
        'Outdoors boundary condition and a Wall face type for their parent face.'
    )

    overhead_construction: Union[OpaqueConstruction, None] = Field(
        default=None,
        description='An OpaqueConstruction for opaque doors with an '
        'Outdoors boundary condition and a RoofCeiling or Floor type for '
        'their parent face.'
    )

    exterior_glass_construction: Union[
        WindowConstruction, WindowConstructionShade, WindowConstructionDynamic, None
    ] = Field(
        default=None,
        description='A WindowConstruction for all glass doors with an '
        'Outdoors boundary condition.'
    )

    interior_glass_construction: Union[
        WindowConstruction, WindowConstructionShade, WindowConstructionDynamic, None
    ] = Field(
        default=None,
        description='A WindowConstruction for all glass doors with a '
        'Surface boundary condition.'
    )


class ConstructionSetAbridged(IDdEnergyBaseModel):
    """A set of constructions for different surface types and boundary conditions."""

    type: Literal['ConstructionSetAbridged'] = 'ConstructionSetAbridged'

    wall_set: Union[WallConstructionSetAbridged, None] = Field(
        default=None,
        description='A WallConstructionSetAbridged object for this ConstructionSet.'
    )

    floor_set: Union[FloorConstructionSetAbridged, None] = Field(
        default=None,
        description='A FloorConstructionSetAbridged object for this ConstructionSet.'
    )

    roof_ceiling_set: Union[RoofCeilingConstructionSetAbridged, None] = Field(
        default=None,
        description='A RoofCeilingConstructionSetAbridged object for this '
        'ConstructionSet.'
    )

    aperture_set: Union[ApertureConstructionSetAbridged, None] = Field(
        default=None,
        description='A ApertureConstructionSetAbridged object for this ConstructionSet.'
    )

    door_set: Union[DoorConstructionSetAbridged, None] = Field(
        default=None,
        description='A DoorConstructionSetAbridged object for this ConstructionSet.'
    )

    shade_construction: Union[str, None] = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='The identifier of a ShadeConstruction to set the reflectance '
        'properties of all outdoor shades of all objects to which this '
        'ConstructionSet is assigned.'
    )

    air_boundary_construction: Union[str, None] = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='The identifier of an AirBoundaryConstruction or OpaqueConstruction '
        'to set the properties of Faces with an AirBoundary type.'
    )


class ConstructionSet(ConstructionSetAbridged):
    """A set of constructions for different surface types and boundary conditions."""

    type: Literal['ConstructionSet'] = 'ConstructionSet'

    wall_set: Union[WallConstructionSet, None] = Field(
        default=None,
        description='A WallConstructionSet object for this ConstructionSet.'
    )

    floor_set: Union[FloorConstructionSet, None] = Field(
        default=None,
        description='A FloorConstructionSet object for this ConstructionSet.'
    )

    roof_ceiling_set: Union[RoofCeilingConstructionSet, None] = Field(
        default=None,
        description='A RoofCeilingConstructionSet object for this ConstructionSet.'
    )

    aperture_set: Union[ApertureConstructionSet, None] = Field(
        default=None,
        description='A ApertureConstructionSet object for this ConstructionSet.'
    )

    door_set: Union[DoorConstructionSet, None] = Field(
        default=None,
        description='A DoorConstructionSet object for this ConstructionSet.'
    )

    shade_construction: Union[ShadeConstruction, None] = Field(
        default=None,
        description='A ShadeConstruction to set the reflectance '
        'properties of all outdoor shades of all objects to which this '
        'ConstructionSet is assigned.'
    )

    air_boundary_construction: Union[
        AirBoundaryConstruction, OpaqueConstruction, None
    ] = Field(
        default=None,
        description='An AirBoundaryConstruction or OpaqueConstruction to set '
        'the properties of Faces with an AirBoundary type.'
    )
