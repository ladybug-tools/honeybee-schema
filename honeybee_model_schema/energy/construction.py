"""Construction Schema"""
from pydantic import BaseModel, Field, constr
from typing import List, Union

from ._base import NamedEnergyBaseModel
from .material import EnergyMaterial, EnergyMaterialNoMass, \
    EnergyWindowMaterialGas, EnergyWindowMaterialGasCustom, \
    EnergyWindowMaterialGasMixture, EnergyWindowMaterialSimpleGlazSys, \
    EnergyWindowMaterialBlind, EnergyWindowMaterialGlazing, EnergyWindowMaterialShade


class WindowConstructionAbridged(NamedEnergyBaseModel):
    """Construction for window objects (Aperture, Door)."""

    type: constr(regex='^WindowConstructionAbridged$') = 'WindowConstructionAbridged'

    layers: List[constr(min_length=1, max_length=100)] = Field(
        ...,
        description='List of strings for material names. The order of the materials '
            'is from exterior to interior.',
        min_items=1,
        max_items=8
    )


class WindowConstruction(WindowConstructionAbridged):
    """Construction for window objects (Aperture, Door)."""

    type: constr(regex='^WindowConstruction$') = 'WindowConstruction'

    materials: List[
        Union[
            EnergyWindowMaterialGas, EnergyWindowMaterialGasCustom, EnergyWindowMaterialGasMixture,
            EnergyWindowMaterialSimpleGlazSys, EnergyWindowMaterialBlind,
            EnergyWindowMaterialGlazing, EnergyWindowMaterialShade
        ]
    ] = Field(
        ...,
        description='List of materials. The order of the materials is from outside '
            'to inside.',
        min_items=1,
        max_items=8
    )


class OpaqueConstructionAbridged(NamedEnergyBaseModel):
    """Construction for opaque objects (Face, Shade, Door)."""

    type: constr(regex='^OpaqueConstructionAbridged$') = 'OpaqueConstructionAbridged'

    layers: List[constr(min_length=1, max_length=100)] = Field(
        ...,
        description='List of strings for material names. The order of the materials '
            'is from exterior to interior.',
        min_items=1,
        max_items=10
    )


class OpaqueConstruction(OpaqueConstructionAbridged):
    """Construction for opaque objects (Face, Shade, Door)."""

    type: constr(regex='^OpaqueConstruction$') = 'OpaqueConstruction'

    materials: List[Union[EnergyMaterial, EnergyMaterialNoMass]] = Field(
        ...,
        description='List of materials. The order of the materials is from outside to'
        ' inside.',
        min_items=1,
        max_items=10
    )


class ShadeConstruction(NamedEnergyBaseModel):
    """Construction for Shade objects."""

    type: constr(regex='^ShadeConstruction$') = 'ShadeConstruction'

    solar_reflectance: float = Field(
        0.2,
        ge=0,
        le=1,
        description=' A number for the solar reflectance of the construction.'
    )

    visible_reflectance: float = Field(
        0.2,
        ge=0,
        le=1,
        description=' A number for the visible reflectance of the construction.'
    )

    is_specular: bool = Field(
        default=False,
        description='Boolean to note whether the reflection off the shade is diffuse '
            '(False) or specular (True). Set to True if the construction is '
            'representing a glass facade or a mirror material.'
    )


if __name__ == '__main__':
    print(WindowConstructionAbridged.schema_json(indent=2))
    print(WindowConstruction.schema_json(indent=2))
    print(OpaqueConstructionAbridged.schema_json(indent=2))
    print(OpaqueConstruction.schema_json(indent=2))
    print(ShadeConstruction.schema_json(indent=2))
