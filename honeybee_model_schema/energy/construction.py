"""Construction Schema"""
from pydantic import BaseModel, Schema, validator, ValidationError, constr
from typing import List, Union
from enum import Enum
from .materials import EnergyMaterial, EnergyMaterialNoMass, \
    EnergyWindowMaterialGas, EnergyWindowMaterialGasCustom, \
    EnergyWindowMaterialGasMixture, EnergyWindowMaterialSimpleGlazSys, \
    EnergyWindowMaterialBlind, EnergyWindowMaterialGlazing, EnergyWindowMaterialShade


class WindowConstructionAbridged(BaseModel):
    """
    Group of objects to describe the physical properties and configuration for
    the building envelope and interior elements that is the windows of the building.
    """
    type: Enum('WindowConstructionAbridged', {
               'type': 'WindowConstructionAbridged'})

    name: str = Schema(
        ...,
        min_length=1,
        max_length=100
    )

    @validator('name')
    def check_name(cls, v):
        assert all(ord(i) < 128 for i in v), 'Name contains non ASCII characters.'
        assert all(char not in v for char in (',', ';', '!', '\n', '\t')), \
            'Name contains invalid character for EnergyPlus (, ; ! \n \t).'
        assert len(v) > 0, 'Name is an empty string.'
        assert len(v) <= 100, 'Number of characters must be less than 100.'

    layers: List[constr(min_length=1, max_length=100)] = Schema(
        ...,
        description='List of materials. The order of the materials is from outside to'
        ' inside.',
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
                'Window construction cannot have more than 8 materials.'
            )
        else:
            return layers


class WindowConstruction(WindowConstructionAbridged):
    """
    Group of objects to describe the physical properties and configuration for
    the building envelope and interior elements that is the windows of the building.

    """
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
        description='List of materials. The order of the materials is from outside to'
        ' inside.',
        minItems=1,
        maxItems=8
    )

    @validator('materials', whole=True)
    def check_num_items(cls, materials):
        "Ensure length of material is at least 1 and not more than 8."
        if len(materials) == 0:
            raise ValidationError(
                'Window construction should at least have one material.'
            )

        elif len(materials) > 8:
            raise ValidationError(
                'Window construction cannot have more than 8 materials.'
            )
        else:
            return materials


class OpaqueConstructionAbridged(BaseModel):
    """
    Group of objects to describe the physical properties and configuration for
    the building envelope and interior elements that is the walls, roofs, floors,
    and doors of the building.
    """
    type: Enum('OpaqueConstructionAbridged', {
               'type': 'OpaqueConstructionAbridged'})

    name: str = Schema(
        ...,
        min_length=1,
        max_length=100
    )

    @validator('name')
    def check_name(cls, v):
        assert all(ord(i) < 128 for i in v), 'Name contains non ASCII characters.'
        assert all(char not in v for char in (',', ';', '!', '\n', '\t')), \
            'Name contains invalid character for EnergyPlus (, ; ! \n \t).'
        assert len(v) > 0, 'Name is an empty string.'
        assert len(v) <= 100, 'Number of characters must be less than 100.'

    layers: List[constr(min_length=1, max_length=100)] = Schema(
        ...,
        description='List of materials. The order of the materials is from outside to'
        ' inside.',
        minItems=1,
        maxItems=10
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
                'Opaque construction cannot have more than 10 materials.'
            )
        else:
            return layers


class OpaqueConstruction(OpaqueConstructionAbridged):
    """
    Group of objects to describe the physical properties and configuration for
    the building envelope and interior elements that is the walls, roofs, floors,
    and doors of the building.
    """
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

    @validator('materials', whole=True)
    def check_num_items(cls, materials):
        "Ensure length of material is at least 1 and not more than 10."
        if len(materials) == 0:
            raise ValidationError(
                'Opaque construction should at least have one material.'
            )
        elif len(materials) > 10:
            raise ValidationError(
                'Opaque construction cannot have more than 10 materials.'
            )
        else:
            return materials


class ShadeConstruction(BaseModel):

    type: Enum('ShadeConstruction', {
               'type': 'ShadeConstruction'})

    name: str = Schema(
        ...,
        min_length=1,
        max_length=100
    )

    @validator('name')
    def check_name(cls, v):
        assert all(ord(i) < 128 for i in v), 'Name contains non ASCII characters.'
        assert all(char not in v for char in (',', ';', '!', '\n', '\t')), \
            'Name contains invalid character for EnergyPlus (, ; ! \n \t).'
        assert len(v) > 0, 'Name is an empty string.'
        assert len(v) <= 100, 'Number of characters must be less than 100.'

    solar_reflectance: float = Schema(
        0,
        ge=0,
        le=1
    )

    visible_reflectance: float = Schema(
        0,
        ge=0,
        le=1
    )

    is_specular: bool


if __name__ == '__main__':
    print(WindowConstructionAbridged.schema_json(indent=2))


if __name__ == '__main__':
    print(WindowConstruction.schema_json(indent=2))

if __name__ == '__main__':
    print(OpaqueConstructionAbridged.schema_json(indent=2))


if __name__ == '__main__':
    print(OpaqueConstruction.schema_json(indent=2))

if __name__ == '__main__':
    print(ShadeConstruction.schema_json(indent=2))
