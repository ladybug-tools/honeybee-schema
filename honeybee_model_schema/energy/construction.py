"""Construction Schema"""
from pydantic import BaseModel, Schema, validator, ValidationError, constr
from typing import List, Union
from enum import Enum

from ._base import NamedEnergyBaseModel
from .material import EnergyMaterial, EnergyMaterialNoMass, \
    EnergyWindowMaterialGas, EnergyWindowMaterialGasCustom, \
    EnergyWindowMaterialGasMixture, EnergyWindowMaterialSimpleGlazSys, \
    EnergyWindowMaterialBlind, EnergyWindowMaterialGlazing, EnergyWindowMaterialShade


class WindowConstructionAbridged(NamedEnergyBaseModel):
    """Construction for window objects (Aperture, Door)."""

    type: Enum('WindowConstructionAbridged', {
               'type': 'WindowConstructionAbridged'})

    layers: List[constr(min_length=1, max_length=100)] = Schema(
        ...,
        description='List of strings for material names. The order of the materials '
            'is from exterior to interior.',
        minItems=1,
        maxItems=8
    )

    @validator('layers', whole=True)
    def check_num_items(cls, layers):
        "Ensure length of material is at least 1 and not more than 8."
        if len(layers) == 0:
            raise ValidationError(
                'Window construction should at least have one material.'
            )

        elif len(layers) > 8:
            raise ValidationError(
                'Window construction cannot have more than 8 layers.'
            )
        else:
            return layers


class WindowConstruction(WindowConstructionAbridged):
    """Construction for window objects (Aperture, Door)."""

    type: Enum('WindowConstruction', {
               'type': 'WindowConstruction'})

    materials: List[
        Union[
            EnergyWindowMaterialGas, EnergyWindowMaterialGasCustom, EnergyWindowMaterialGasMixture,
            EnergyWindowMaterialSimpleGlazSys, EnergyWindowMaterialBlind,
            EnergyWindowMaterialGlazing, EnergyWindowMaterialShade
        ]
    ] = Schema(
        ...,
        description='List of materials. The order of the materials is from outside '
            'to inside.',
        minItems=1,
        maxItems=8
    )


class OpaqueConstructionAbridged(NamedEnergyBaseModel):
    """Construction for opaque objects (Face, Shade, Door)."""

    type: Enum('OpaqueConstructionAbridged', {
               'type': 'OpaqueConstructionAbridged'})

    layers: List[constr(min_length=1, max_length=100)] = Schema(
        ...,
        description='List of strings for material names. The order of the materials '
            'is from exterior to interior.',
        min_items=1,
        max_items=10
    )

    @validator('layers', whole=True)
    def check_num_items(cls, layers):
        "Ensure length of material is at least 1 and not more than 10."
        if len(layers) == 0:
            raise ValidationError(
                'Opaque construction should at least have one material.'
            )
        elif len(layers) > 10:
            raise ValidationError(
                'Opaque construction cannot have more than 10 layers.'
            )
        else:
            return layers


class OpaqueConstruction(OpaqueConstructionAbridged):
    """Construction for opaque objects (Face, Shade, Door)."""

    type: Enum('OpaqueConstruction', {
               'type': 'OpaqueConstruction'})

    materials: List[
        Union[
            EnergyMaterial, EnergyMaterialNoMass
        ]
    ] = Schema(
        ...,
        description='List of materials. The order of the materials is from outside to'
        ' inside.',
        minItems=1,
        maxItems=10
    )


class ShadeConstruction(NamedEnergyBaseModel):
    """Construction for Shade objects."""

    type: Enum('ShadeConstruction', {
               'type': 'ShadeConstruction'})

    solar_reflectance: float = Schema(
        0.2,
        ge=0,
        le=1,
        description=' A number for the solar reflectance of the construction.'
    )

    visible_reflectance: float = Schema(
        0.2,
        ge=0,
        le=1,
        description=' A number for the visible reflectance of the construction.'
    )

    is_specular: bool = Schema(
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
