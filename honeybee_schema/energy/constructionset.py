"""ConstructionSet Schema"""
from pydantic import Field, constr
from typing import List, Union

from .._base import NoExtraBaseModel
from ._base import IDdEnergyBaseModel
from .construction import OpaqueConstructionAbridged, WindowConstructionAbridged, \
    ShadeConstruction, AirBoundaryConstructionAbridged
from .material import EnergyMaterial, EnergyMaterialNoMass, \
    EnergyWindowMaterialGas, EnergyWindowMaterialGasCustom, \
    EnergyWindowMaterialGasMixture, EnergyWindowMaterialSimpleGlazSys, \
    EnergyWindowMaterialBlind, EnergyWindowMaterialGlazing, EnergyWindowMaterialShade


class WallSetAbridged(NoExtraBaseModel):
    """A set of constructions for wall assemblies."""

    type: constr(regex='^WallSetAbridged$') = 'WallSetAbridged'

    interior_construction: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier for an OpaqueConstruction for walls with a Surface or '
            'Adiabatic boundary condition.'
    )

    exterior_construction: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier for an OpaqueConstruction for walls with an Outdoors '
            'boundary condition.'
    )

    ground_construction: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier for an OpaqueConstruction for walls with a Ground '
            'boundary condition.'
    )


class FloorSetAbridged(NoExtraBaseModel):
    """A set of constructions for floor assemblies."""

    type: constr(regex='^FloorSetAbridged$') = 'FloorSetAbridged'

    interior_construction: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier for an OpaqueConstruction for floors with a Surface or '
            'Adiabatic boundary condition.'
    )

    exterior_construction: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier for an OpaqueConstruction for floors with an Outdoors '
            'boundary condition.'
    )

    ground_construction: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier for an OpaqueConstruction for floors with a Ground '
            'boundary condition.'
    )


class RoofCeilingSetAbridged(NoExtraBaseModel):
    """A set of constructions for roof and ceiling assemblies."""

    type: constr(regex='^RoofCeilingSetAbridged$') = 'RoofCeilingSetAbridged'

    interior_construction: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier for an OpaqueConstruction for ceilings with a Surface or '
            'Adiabatic boundary condition.'
    )

    exterior_construction: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier for an OpaqueConstruction for roofs with an Outdoors '
            'boundary condition.'
    )

    ground_construction: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier for an OpaqueConstruction for roofs with a Ground '
            'boundary condition.'
    )


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


class ConstructionSetAbridged(IDdEnergyBaseModel):
    """A set of constructions for different surface types and boundary conditions."""

    type: constr(regex='^ConstructionSetAbridged$') = 'ConstructionSetAbridged'

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

    materials: List[
        Union[
            EnergyMaterial, EnergyMaterialNoMass,
            EnergyWindowMaterialGas, EnergyWindowMaterialGasMixture,
            EnergyWindowMaterialGasCustom, EnergyWindowMaterialBlind,
            EnergyWindowMaterialGlazing, EnergyWindowMaterialShade,
            EnergyWindowMaterialSimpleGlazSys]
        ] = Field(
                ...,
                description='List of materials. The order of the materials is from '
                    'outside to inside.',
                min_items=1,
                max_items=8
            )

    constructions:  List[
        Union[
            OpaqueConstructionAbridged, WindowConstructionAbridged,
            ShadeConstruction, AirBoundaryConstructionAbridged
        ]] = Field(
                ...,
                description='List of abridged Construction objects.',
            )


if __name__ == '__main__':
    print(ConstructionSetAbridged.schema_json(indent=2))
    print(ConstructionSet.schema_json(indent=2))
