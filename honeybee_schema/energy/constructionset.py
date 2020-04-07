"""ConstructionSet Schema"""
from pydantic import Field, constr
from typing import List, Union

from .._base import NoExtraBaseModel
from ._base import IDdEnergyBaseModel
from .construction import OpaqueConstructionAbridged, WindowConstructionAbridged, \
    ShadeConstruction, AirBoundaryConstructionAbridged, OpaqueConstruction, \
    WindowConstruction, AirBoundaryConstruction
from .material import EnergyMaterial, EnergyMaterialNoMass, \
    EnergyWindowMaterialGas, EnergyWindowMaterialGasCustom, \
    EnergyWindowMaterialGasMixture, EnergyWindowMaterialSimpleGlazSys, \
    EnergyWindowMaterialBlind, EnergyWindowMaterialGlazing, EnergyWindowMaterialShade

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


class WallSetAbridged(_FaceSubSetAbridged):
    """A set of constructions for wall assemblies."""

    type: constr(regex='^WallSetAbridged$') = 'WallSetAbridged'


class FloorSetAbridged(_FaceSubSetAbridged):
    """A set of constructions for floor assemblies."""

    type: constr(regex='^FloorSetAbridged$') = 'FloorSetAbridged'


class RoofCeilingSetAbridged(_FaceSubSetAbridged):
    """A set of constructions for roof and ceiling assemblies."""

    type: constr(regex='^RoofCeilingSetAbridged$') = 'RoofCeilingSetAbridged'


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


class WallSet(_FaceSubSet):
    """A set of constructions for wall assemblies."""

    type: constr(regex='^WallSet$') = 'WallSet'


class FloorSet(_FaceSubSet):
    """A set of constructions for floor assemblies."""

    type: constr(regex='^FloorSet$') = 'FloorSet'


class RoofCeilingSet(_FaceSubSet):
    """A set of constructions for roof and ceiling assemblies."""

    type: constr(regex='^RoofCeilingSet$') = 'RoofCeilingSet'


class ApertureSetAbridged(NoExtraBaseModel):
    """A set of constructions for aperture assemblies."""

    type: constr(regex='^ApertureSetAbridged$') = 'ApertureSetAbridged'

    interior_construction: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier for a WindowConstruction for apertures with an '
            'Outdoors boundary condition, False is_operable property, and a Wall '
            'face type for their parent face.'
    )

    window_construction: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier for a WindowConstruction for all apertures with a '
            'Surface boundary condition.'
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
            'Outdoors boundary condition and True is_operable property..'
    )


class ApertureSet(NoExtraBaseModel):
    """A set of constructions for aperture assemblies."""

    type: constr(regex='^ApertureSet$') = 'ApertureSet'

    interior_construction: WindowConstruction = Field(
        default=None,
        description='A WindowConstruction for apertures with an '
            'Outdoors boundary condition, False is_operable property, and a Wall '
            'face type for their parent face.'
    )

    window_construction: WindowConstruction = Field(
        default=None,
        description='A WindowConstruction for all apertures with a '
            'Surface boundary condition.'
    )

    skylight_construction: WindowConstruction = Field(
        default=None,
        description='A WindowConstruction for apertures with a Outdoors boundary '
            'condition, False is_operable property, and a RoofCeiling or '
            'Floor face type for their parent face.'
    )

    operable_construction: WindowConstruction = Field(
        default=None,
        description='A WindowConstruction for all apertures with an '
            'Outdoors boundary condition and True is_operable property..'
    )


class DoorSetAbridged(NoExtraBaseModel):
    """A set of constructions for door assemblies."""

    type: constr(regex='^DoorSetAbridged$') = 'DoorSetAbridged'

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


class DoorSet(NoExtraBaseModel):
    """A set of constructions for door assemblies."""

    type: constr(regex='^DoorSet$') = 'DoorSet'

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

    exterior_glass_construction: WindowConstruction = Field(
        default=None,
        description='A WindowConstruction for all glass doors with an '
            'Outdoors boundary condition.'
    )

    interior_glass_construction: WindowConstruction = Field(
        default=None,
        description='A WindowConstruction for all glass doors with a '
            'Surface boundary condition.'
    )


class ConstructionSetAbridged(IDdEnergyBaseModel):
    """A set of constructions for different surface types and boundary conditions."""

    type: constr(regex='^ConstructionSetAbridged$') = 'ConstructionSetAbridged'

    wall_set: WallSetAbridged = Field(
        default=None,
        description='A WallSetAbridged object for this ConstructionSet.'
    )

    floor_set: FloorSetAbridged = Field(
        default=None,
        description='A FloorSetAbridged object for this ConstructionSet.'
    )

    roof_ceiling_set: RoofCeilingSetAbridged = Field(
        default=None,
        description='A RoofCeilingSetAbridged object for this ConstructionSet.'
    )

    aperture_set: ApertureSetAbridged = Field(
        default=None,
        description='A ApertureSetAbridged object for this ConstructionSet.'
    )

    door_set: DoorSetAbridged = Field(
        default=None,
        description='A DoorSetAbridged object for this ConstructionSet.'
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
        description='The identifier of an AirBoundaryConstruction to set the properties '
            'of Faces with an AirBoundary type.'
    )


class ConstructionSet(ConstructionSetAbridged):
    """A set of constructions for different surface types and boundary conditions."""

    type: constr(regex='^ConstructionSet$') = 'ConstructionSet'

    wall_set: WallSet = Field(
        default=None,
        description='A WallSet object for this ConstructionSet.'
    )

    floor_set: FloorSet = Field(
        default=None,
        description='A FloorSet object for this ConstructionSet.'
    )

    roof_ceiling_set: RoofCeilingSet = Field(
        default=None,
        description='A RoofCeilingSet object for this ConstructionSet.'
    )

    aperture_set: ApertureSet = Field(
        default=None,
        description='A ApertureSet object for this ConstructionSet.'
    )

    door_set: DoorSet = Field(
        default=None,
        description='A DoorSet object for this ConstructionSet.'
    )

    shade_construction: ShadeConstruction = Field(
        default=None,
        description='A ShadeConstruction to set the reflectance '
            'properties of all outdoor shades of all objects to which this '
            'ConstructionSet is assigned.'
    )

    air_boundary_construction: AirBoundaryConstruction = Field(
        default=None,
        description='An AirBoundaryConstruction to set the properties '
            'of Faces with an AirBoundary type.'
    )


if __name__ == '__main__':
    print(ConstructionSetAbridged.schema_json(indent=2))
    print(ConstructionSet.schema_json(indent=2))
