"""ConstructionSet Schema"""
from pydantic import Field, constr
from typing import Union

from .._base import NoExtraBaseModel
from ._base import IDdEnergyBaseModel
from .construction import OpaqueConstruction, WindowConstruction, ShadeConstruction, \
    AirBoundaryConstruction, WindowConstructionShade, WindowConstructionDynamic


class _FaceSubSetAbridged(NoExtraBaseModel):
    """A set of constructions for wall, floor, or roof assemblies."""

    interior_construction: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier for an OpaqueConstruction for faces with a Surface or '
        'Adiabatic boundary condition.'
    )

    exterior_construction: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier for an OpaqueConstruction for faces with an Outdoors '
        'boundary condition.'
    )

    ground_construction: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier for an OpaqueConstruction for faces with a Ground '
        'boundary condition.'
    )


class WallConstructionSetAbridged(_FaceSubSetAbridged):
    """A set of constructions for wall assemblies."""

    type: constr(regex='^WallConstructionSetAbridged$') = \
        'WallConstructionSetAbridged'


class FloorConstructionSetAbridged(_FaceSubSetAbridged):
    """A set of constructions for floor assemblies."""

    type: constr(regex='^FloorConstructionSetAbridged$') = \
        'FloorConstructionSetAbridged'


class RoofCeilingConstructionSetAbridged(_FaceSubSetAbridged):
    """A set of constructions for roof and ceiling assemblies."""

    type: constr(regex='^RoofCeilingConstructionSetAbridged$') = \
        'RoofCeilingConstructionSetAbridged'


class _FaceSubSet(NoExtraBaseModel):
    """A set of constructions for wall, floor, or roof assemblies."""

    interior_construction: OpaqueConstruction = Field(
        default=None,
        description='An OpaqueConstruction for walls with a Surface or '
        'Adiabatic boundary condition.'
    )

    exterior_construction: OpaqueConstruction = Field(
        default=None,
        description='An OpaqueConstruction for walls with an Outdoors '
        'boundary condition.'
    )

    ground_construction: OpaqueConstruction = Field(
        default=None,
        description='An OpaqueConstruction for walls with a Ground '
        'boundary condition.'
    )


class WallConstructionSet(_FaceSubSet):
    """A set of constructions for wall assemblies."""

    type: constr(regex='^WallConstructionSet$') = 'WallConstructionSet'


class FloorConstructionSet(_FaceSubSet):
    """A set of constructions for floor assemblies."""

    type: constr(regex='^FloorConstructionSet$') = 'FloorConstructionSet'


class RoofCeilingConstructionSet(_FaceSubSet):
    """A set of constructions for roof and ceiling assemblies."""

    type: constr(regex='^RoofCeilingConstructionSet$') = 'RoofCeilingConstructionSet'


class ApertureConstructionSetAbridged(NoExtraBaseModel):
    """A set of constructions for aperture assemblies."""

    type: constr(regex='^ApertureConstructionSetAbridged$') = \
        'ApertureConstructionSetAbridged'

    interior_construction: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier for a WindowConstruction for all apertures with a '
        'Surface boundary condition.'
    )

    window_construction: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier for a WindowConstruction for apertures with an '
        'Outdoors boundary condition, False is_operable property, and a Wall '
        'face type for their parent face.'
    )

    skylight_construction: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier for a WindowConstruction for apertures with a Outdoors '
        'boundary condition, False is_operable property, and a RoofCeiling or '
        'Floor face type for their parent face.'
    )

    operable_construction: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier for a WindowConstruction for all apertures with an '
        'Outdoors boundary condition and True is_operable property.'
    )


class ApertureConstructionSet(NoExtraBaseModel):
    """A set of constructions for aperture assemblies."""

    type: constr(regex='^ApertureConstructionSet$') = 'ApertureConstructionSet'

    interior_construction: Union[
        WindowConstruction, WindowConstructionShade, WindowConstructionDynamic
    ] = Field(
        default=None, description='A WindowConstruction for all apertures with a '
        'Surface boundary condition.'
    )

    window_construction: Union[
        WindowConstruction, WindowConstructionShade, WindowConstructionDynamic
    ] = Field(
        default=None, description='A WindowConstruction for apertures with an '
        'Outdoors boundary condition, False is_operable property, and a Wall '
        'face type for their parent face.'
    )

    skylight_construction: Union[
        WindowConstruction, WindowConstructionShade, WindowConstructionDynamic
    ] = Field(
        default=None,
        description='A WindowConstruction for apertures with a Outdoors boundary '
        'condition, False is_operable property, and a RoofCeiling or '
        'Floor face type for their parent face.'
    )

    operable_construction: Union[
        WindowConstruction, WindowConstructionShade, WindowConstructionDynamic
    ] = Field(
        default=None,
        description='A WindowConstruction for all apertures with an '
        'Outdoors boundary condition and True is_operable property.'
    )


class DoorConstructionSetAbridged(NoExtraBaseModel):
    """A set of constructions for door assemblies."""

    type: constr(regex='^DoorConstructionSetAbridged$') = 'DoorConstructionSetAbridged'

    interior_construction: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier for an OpaqueConstruction for all opaque doors with a '
        'Surface boundary condition.'
    )

    exterior_construction: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier for an OpaqueConstruction for opaque doors with an '
        'Outdoors boundary condition and a Wall face type for their parent face.'
    )

    overhead_construction: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier for an OpaqueConstruction for opaque doors with an '
        'Outdoors boundary condition and a RoofCeiling or Floor type for '
        'their parent face.'
    )

    exterior_glass_construction: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier for a WindowConstruction for all glass doors with an '
        'Outdoors boundary condition.'
    )

    interior_glass_construction: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier for a WindowConstruction for all glass doors with a '
        'Surface boundary condition.'
    )


class DoorConstructionSet(NoExtraBaseModel):
    """A set of constructions for door assemblies."""

    type: constr(regex='^DoorConstructionSet$') = 'DoorConstructionSet'

    interior_construction: OpaqueConstruction = Field(
        default=None,
        description='An OpaqueConstruction for all opaque doors with a '
        'Surface boundary condition.'
    )

    exterior_construction: OpaqueConstruction = Field(
        default=None,
        description='An OpaqueConstruction for opaque doors with an '
        'Outdoors boundary condition and a Wall face type for their parent face.'
    )

    overhead_construction: OpaqueConstruction = Field(
        default=None,
        description='An OpaqueConstruction for opaque doors with an '
        'Outdoors boundary condition and a RoofCeiling or Floor type for '
        'their parent face.'
    )

    exterior_glass_construction: Union[
        WindowConstruction, WindowConstructionShade, WindowConstructionDynamic
    ] = Field(
        default=None,
        description='A WindowConstruction for all glass doors with an '
        'Outdoors boundary condition.'
    )

    interior_glass_construction: Union[
        WindowConstruction, WindowConstructionShade, WindowConstructionDynamic
    ] = Field(
        default=None,
        description='A WindowConstruction for all glass doors with a '
        'Surface boundary condition.'
    )


class ConstructionSetAbridged(IDdEnergyBaseModel):
    """A set of constructions for different surface types and boundary conditions."""

    type: constr(regex='^ConstructionSetAbridged$') = 'ConstructionSetAbridged'

    wall_set: WallConstructionSetAbridged = Field(
        default=None,
        description='A WallConstructionSetAbridged object for this ConstructionSet.'
    )

    floor_set: FloorConstructionSetAbridged = Field(
        default=None,
        description='A FloorConstructionSetAbridged object for this ConstructionSet.'
    )

    roof_ceiling_set: RoofCeilingConstructionSetAbridged = Field(
        default=None,
        description='A RoofCeilingConstructionSetAbridged object for this '
        'ConstructionSet.'
    )

    aperture_set: ApertureConstructionSetAbridged = Field(
        default=None,
        description='A ApertureConstructionSetAbridged object for this ConstructionSet.'
    )

    door_set: DoorConstructionSetAbridged = Field(
        default=None,
        description='A DoorConstructionSetAbridged object for this ConstructionSet.'
    )

    shade_construction: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='The identifier of a ShadeConstruction to set the reflectance '
        'properties of all outdoor shades of all objects to which this '
        'ConstructionSet is assigned.'
    )

    air_boundary_construction: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='The identifier of an AirBoundaryConstruction or OpaqueConstruction '
        'to set the properties of Faces with an AirBoundary type.'
    )


class ConstructionSet(ConstructionSetAbridged):
    """A set of constructions for different surface types and boundary conditions."""

    type: constr(regex='^ConstructionSet$') = 'ConstructionSet'

    wall_set: WallConstructionSet = Field(
        default=None,
        description='A WallConstructionSet object for this ConstructionSet.'
    )

    floor_set: FloorConstructionSet = Field(
        default=None,
        description='A FloorConstructionSet object for this ConstructionSet.'
    )

    roof_ceiling_set: RoofCeilingConstructionSet = Field(
        default=None,
        description='A RoofCeilingConstructionSet object for this ConstructionSet.'
    )

    aperture_set: ApertureConstructionSet = Field(
        default=None,
        description='A ApertureConstructionSet object for this ConstructionSet.'
    )

    door_set: DoorConstructionSet = Field(
        default=None,
        description='A DoorConstructionSet object for this ConstructionSet.'
    )

    shade_construction: ShadeConstruction = Field(
        default=None,
        description='A ShadeConstruction to set the reflectance '
        'properties of all outdoor shades of all objects to which this '
        'ConstructionSet is assigned.'
    )

    air_boundary_construction: Union[
        AirBoundaryConstruction, OpaqueConstruction
    ] = Field(
        default=None,
        description='An AirBoundaryConstruction or OpaqueConstruction to set '
        'the properties of Faces with an AirBoundary type.'
    )
