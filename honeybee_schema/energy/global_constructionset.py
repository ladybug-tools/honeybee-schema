"""Global construction-set for Model."""
import pathlib
import json

from typing import List, Union, Literal
from pydantic import Field

from honeybee_standards import energy_default

from .._base import NoExtraBaseModel
from .constructionset import WallConstructionSetAbridged, FloorConstructionSetAbridged, \
    RoofCeilingConstructionSetAbridged, ApertureConstructionSetAbridged, \
    DoorConstructionSetAbridged
from .construction import OpaqueConstructionAbridged, WindowConstructionAbridged, \
    ShadeConstruction, AirBoundaryConstructionAbridged
from .material import EnergyMaterial, EnergyMaterialNoMass, \
    EnergyWindowMaterialGlazing, EnergyWindowMaterialGas


# import constructionset default values from honeybee standards
_DEFAULTS = json.loads(pathlib.Path(energy_default).read_text())
_CSET = [
    ms for ms in _DEFAULTS['construction_sets']
    if ms['identifier'] == 'Default Generic Construction Set'][0]
_CONSTRUCTION_NAMES = [
    'Generic Exterior Wall', 'Generic Interior Wall', 'Generic Underground Wall',
    'Generic Exposed Floor', 'Generic Interior Floor', 'Generic Ground Slab',
    'Generic Roof', 'Generic Interior Ceiling', 'Generic Underground Roof',
    'Generic Double Pane', 'Generic Single Pane', 'Generic Exterior Door',
    'Generic Interior Door', 'Generic Shade', 'Generic Context', 'Generic Air Boundary'
]
_CONSTRUCTIONS = [ # type: ignore
    OpaqueConstructionAbridged.model_validate(m)
    if m['type'] == 'OpaqueConstructionAbridged'
    else WindowConstructionAbridged.model_validate(m)
    if m['type'] == 'WindowConstructionAbridged'
    else ShadeConstruction.model_validate(m)
    if m['type'] == 'ShadeConstruction'
    else AirBoundaryConstructionAbridged.model_validate(m)
    for m in _DEFAULTS['constructions'] if m['identifier'] in _CONSTRUCTION_NAMES
]
_MATERIAL_NAMES = [
    'Generic 25mm Wood', 'Generic Clear Glass', 'Generic LW Concrete',
    'Generic Ceiling Air Gap', 'Generic Acoustic Tile', 'Generic Gypsum Board',
    'Generic Wall Air Gap', 'Generic Painted Metal', 'Generic 50mm Insulation',
    'Generic Roof Membrane', 'Generic Brick', 'Generic HW Concrete',
    'Generic Low-e Glass', 'Generic Window Air Gap', 'Generic 25mm Insulation'
]
_MATERIALS = [ # type: ignore
    EnergyMaterial.model_validate(m)
    if m['type'] == 'EnergyMaterial'
    else EnergyMaterialNoMass.model_validate(m)
    if m['type'] == 'EnergyMaterialNoMass'
    else EnergyWindowMaterialGlazing.model_validate(m)
    if m['type'] == 'EnergyWindowMaterialGlazing'
    else EnergyWindowMaterialGas.model_validate(m)
    for m in _DEFAULTS['materials'] if m['identifier'] in _MATERIAL_NAMES
]


class GlobalConstructionSet(NoExtraBaseModel):

    type: Literal['GlobalConstructionSet'] = 'GlobalConstructionSet'

    materials: List[Union[
        EnergyMaterial, EnergyMaterialNoMass,
        EnergyWindowMaterialGlazing, EnergyWindowMaterialGas
    ]] = Field(
        default=_MATERIALS,
        description='Global Honeybee Energy materials.',
        json_schema_extra={'readOnly': True}
    )

    constructions: List[Union[
        OpaqueConstructionAbridged, WindowConstructionAbridged,
        ShadeConstruction, AirBoundaryConstructionAbridged
    ]] = Field(
        default=_CONSTRUCTIONS,
        description='Global Honeybee Energy constructions.',
        json_schema_extra={'readOnly': True}
    )

    wall_set: WallConstructionSetAbridged = Field(
        default=WallConstructionSetAbridged.model_validate(_CSET['wall_set']),
        description='Global Honeybee WallConstructionSet.',
        json_schema_extra={'readOnly': True}
    )

    floor_set: FloorConstructionSetAbridged = Field(
        default=FloorConstructionSetAbridged.model_validate(_CSET['floor_set']),
        description='Global Honeybee FloorConstructionSet.',
        json_schema_extra={'readOnly': True}
    )

    roof_ceiling_set: RoofCeilingConstructionSetAbridged = Field(
        default=RoofCeilingConstructionSetAbridged.model_validate(_CSET['roof_ceiling_set']),
        description='Global Honeybee RoofCeilingConstructionSet.',
        json_schema_extra={'readOnly': True}
    )

    aperture_set: ApertureConstructionSetAbridged = Field(
        default=ApertureConstructionSetAbridged.model_validate(_CSET['aperture_set']),
        description='Global Honeybee ApertureConstructionSet.',
        json_schema_extra={'readOnly': True}
    )

    door_set: DoorConstructionSetAbridged = Field(
        default=DoorConstructionSetAbridged.model_validate(_CSET['door_set']),
        description='Global Honeybee DoorConstructionSet.',
        json_schema_extra={'readOnly': True}
    )

    shade_construction: str = Field(
        default=_CSET['shade_construction'],
        description='Global Honeybee Construction for building-attached Shades.',
        json_schema_extra={'readOnly': True}
    )

    context_construction: str = Field(
        default='Generic Context',
        description='Global Honeybee Construction for context Shades.',
        json_schema_extra={'readOnly': True}
    )

    air_boundary_construction: str = Field(
        default=_CSET['air_boundary_construction'],
        description='Global Honeybee Construction for AirBoundary Faces.',
        json_schema_extra={'readOnly': True}
    )
