"""ConstructionSet Schema"""
from pydantic import BaseModel, Field
from enum import Enum

from ._base import NamedEnergyBaseModel


class WallSetAbridged(BaseModel):
    """A set of constructions for wall assemblies."""

    type: Enum('WallSetAbridged', {'type': 'WallSetAbridged'})

    interior_construction: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Name for an OpaqueConstruction for walls with a Surface or '
            'Adiabatic boundary condition.'
    )

    exterior_construction: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Name for an OpaqueConstruction for walls with an Outdoors '
            'boundary condition.'
    )

    ground_construction: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Name for an OpaqueConstruction for walls with a Ground '
            'boundary condition.'
    )


class FloorSetAbridged(BaseModel):
    """A set of constructions for floor assemblies."""

    type: Enum('FloorSetAbridged', {'type': 'FloorSetAbridged'})

    interior_construction: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Name for an OpaqueConstruction for floors with a Surface or '
            'Adiabatic boundary condition.'
    )

    exterior_construction: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Name for an OpaqueConstruction for floors with an Outdoors '
            'boundary condition.'
    )

    ground_construction: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Name for an OpaqueConstruction for floors with a Ground '
            'boundary condition.'
    )


class RoofCeilingSetAbridged(BaseModel):
    """A set of constructions for roof and ceiling assemblies."""

    type: Enum('RoofCeilingSetAbridged', {'type': 'RoofCeilingSetAbridged'})

    interior_construction: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Name for an OpaqueConstruction for ceilings with a Surface or '
            'Adiabatic boundary condition.'
    )

    exterior_construction: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Name for an OpaqueConstruction for roofs with an Outdoors '
            'boundary condition.'
    )

    ground_construction: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Name for an OpaqueConstruction for roofs with a Ground '
            'boundary condition.'
    )


class ApertureSetAbridged(BaseModel):
    """A set of constructions for aperture assemblies."""

    type: Enum('ApertureSetAbridged', {'type': 'ApertureSetAbridged'})

    interior_construction: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Name for a WindowConstruction for apertures with an '
            'Outdoors boundary condition, False is_operable property, and a Wall '
            'face type for their parent face.'
    )

    window_construction: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Name for a WindowConstruction for all apertures with a '
            'Surface boundary condition.'
    )

    skylight_construction: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Name for a WindowConstruction for apertures with a Outdoors '
            'boundary condition, False is_operable property, and a RoofCeiling or '
            'Floor face type for their parent face.'
    )

    operable_construction: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Name for a WindowConstruction for all apertures with an '
            'Outdoors boundary condition and True is_operable property..'
    )


class DoorSetAbridged(BaseModel):
    """A set of constructions for door assemblies."""

    type: Enum('DoorSetAbridged', {'type': 'DoorSetAbridged'})

    interior_construction: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Name for an OpaqueConstruction for all opaque doors with a '
            'Surface boundary condition.'
    )

    exterior_construction: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Name for an OpaqueConstruction for opaque doors with an Outdoors '
            'boundary condition and a Wall face type for their parent face.'
    )

    overhead_construction: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Name for an OpaqueConstruction for opaque doors with an Outdoors '
            'boundary condition and a RoofCeiling or Floor type for their parent face.'
    )

    exterior_glass_construction: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Name for an WindowConstruction for all glass doors with an '
            'Outdoors boundary condition.'
    )

    interior_glass_construction: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Name for an WindowConstruction for all glass doors with a '
            'Surface boundary condition.'
    )


class ConstructionSetAbridged(NamedEnergyBaseModel):
    """A set of constructions for different surface types and boundary conditions."""

    type: Enum('ConstructionSetAbridged', {'type': 'ConstructionSetAbridged'})

    wall_set: WallSetAbridged = Field(
        default=None,
        description='A WallSet object for this ConstructionSet.'
    )

    floor_set: FloorSetAbridged = Field(
        default=None,
        description='A FloorSet object for this ConstructionSet.'
    )

    roof_ceiling_set: RoofCeilingSetAbridged = Field(
        default=None,
        description='A RoofCeilingSet object for this ConstructionSet.'
    )

    aperture_set: ApertureSetAbridged = Field(
        default=None,
        description='A ApertureSet object for this ConstructionSet.'
    )

    door_set: DoorSetAbridged = Field(
        default=None,
        description='A DoorSet object for this ConstructionSet.'
    )

    shade_construction: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='A ShadeConstruction to set the reflectance properties of all '
            'outdoor shades to which this ConstructionSet is assigned.'
    )


if __name__ == '__main__':
    print(ConstructionSetAbridged.schema_json(indent=2))
