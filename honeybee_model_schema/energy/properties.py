"""Model energy properties."""
from pydantic import BaseModel, Field
from typing import List, Union
from enum import Enum

from .constructionset import ConstructionSetAbridged
from .construction import OpaqueConstructionAbridged, \
    WindowConstructionAbridged, ShadeConstruction
from .material import EnergyMaterial, EnergyMaterialNoMass, \
    EnergyWindowMaterialGas, EnergyWindowMaterialGasCustom, \
    EnergyWindowMaterialGasMixture, EnergyWindowMaterialSimpleGlazSys, \
    EnergyWindowMaterialBlind, EnergyWindowMaterialGlazing, EnergyWindowMaterialShade
from .programtype import ProgramTypeAbridged
from .load import PeopleAbridged, LightingAbridged, ElectricEquipmentAbridged, \
    GasEquipmentAbridged, InfiltrationAbridged, VentilationAbridged, SetpointAbridged
from .schedule import ScheduleTypeLimit, ScheduleRulesetAbridged, \
    ScheduleFixedIntervalAbridged
from .hvac import IdealAirSystem


class ShadeEnergyPropertiesAbridged(BaseModel):

    type: Enum('ShadeEnergyPropertiesAbridged', {
               'type': 'ShadeEnergyPropertiesAbridged'})

    transmittance_schedule: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Name of a ShadeConstruction to set the reflectance and '
            'specularity of the Shade. If None, the construction is set by the'
            'parent Room construction_set or the Model global_construction_set.'
    )

    construction:  str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Name of a schedule to set the transmittance of the shade, '
            'which can vary throughout the simulation. If None, the shade will '
            'be completely opauqe.'
    )


class DoorEnergyPropertiesAbridged(BaseModel):

    type: Enum('DoorEnergyPropertiesAbridged', {
               'type': 'DoorEnergyPropertiesAbridged'})

    construction: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Name of an OpaqueConstruction or WindowConstruction for the door. '
            'Note that the host door must have the is_glass property set to True '
            'to assign a WindowConstruction. If None, the construction is set by the'
            'parent Room construction_set or the Model global_construction_set.'
    )


class ApertureEnergyPropertiesAbridged(BaseModel):

    type: Enum('ApertureEnergyPropertiesAbridged', {
               'type': 'ApertureEnergyPropertiesAbridged'})

    construction: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Name of a WindowConstruction for the aperture. If None, the '
            'construction is set by the parent Room construction_set or the Model '
            'global_construction_set.'
    )


class FaceEnergyPropertiesAbridged(BaseModel):

    type: Enum('FaceEnergyPropertiesAbridged', {
               'type': 'FaceEnergyPropertiesAbridged'})

    construction: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Name of an OpaqueConstruction for the Face. If None, the '
            'construction is set by the parent Room construction_set or the '
            'Model global_construction_set.'
    )


class RoomEnergyPropertiesAbridged(BaseModel):

    type: Enum('RoomEnergyPropertiesAbridged', {
               'type': 'RoomEnergyPropertiesAbridged'})

    construction_set: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Name of a ConstructionSet to specify all default constructions '
            'for the Faces, Apertures, and Doors of the Room. If None, the Room will '
            'use the Model global_construction_set.'
    )

    program_type: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Name of a ProgramType to specify all default schedules and loads '
            'for the Room. If None, the Room will have no loads or setpoints.'
    )

    hvac: IdealAirSystem = Field(
        default=None
    )

    people: PeopleAbridged = Field(
        default=None,
        description='People object to describe the occupancy of the Room.'
    )
    
    lighting: LightingAbridged = Field(
        default=None,
        description='Lighting object to describe the lighting usage of the Room.'
    )

    electric_equipment: ElectricEquipmentAbridged = Field(
        default=None,
        description='ElectricEquipment object to describe the equipment usage.'
    )

    gas_equipment: GasEquipmentAbridged = Field(
        default=None,
        description='GasEquipment object to describe the equipment usage.'
    )

    infiltration: InfiltrationAbridged = Field(
        default=None,
        description='Infiltration object to to describe the outdoor air leakage.'
    )

    ventilation: VentilationAbridged = Field(
        default=None,
        description='Ventilation object for the minimum outdoor air requirement.'
    )

    setpoint: SetpointAbridged = Field(
        default=None,
        description='Setpoint object for the temperature setpoints of the Room.'
    )


class TerrianTypes(str, Enum):
    ocean = 'Ocean'
    country = 'Country'
    suburbs = 'Suburbs'
    urban = 'Urban'
    city = 'City'


class ModelEnergyProperties(BaseModel):

    type: Enum('ModelEnergyProperties', {'type': 'ModelEnergyProperties'})

    terrain_type: TerrianTypes = TerrianTypes.city

    construction_sets: List[ConstructionSetAbridged] = Field(
        default=None,
        description='List of all ConstructionSets in the Model.'
    )

    global_construction_set: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Name for the ConstructionSet to be used for all objects lacking '
            'their own construction or a parent Room construction_set. This '
            'ConstructionSet must appear under the Model construction_sets.'
    )

    constructions: List[Union[OpaqueConstructionAbridged, WindowConstructionAbridged,
                              ShadeConstruction]] = Field(
        ...,
        description='A list of all unique constructions in the model. This includes '
            'constructions across all Faces, Apertures, Doors, Shades, Room '
            'ConstructionSets, and the global_construction_set.'
    )

    materials: List[Union[EnergyMaterial, EnergyMaterialNoMass, EnergyWindowMaterialGas,
                          EnergyWindowMaterialGasCustom, EnergyWindowMaterialGasMixture,
                          EnergyWindowMaterialSimpleGlazSys, EnergyWindowMaterialBlind,
                          EnergyWindowMaterialGlazing,
                          EnergyWindowMaterialShade]] = Field(
        ...,
        description='A list of all unique materials in the model. This includes '
            'materials needed to make the Model constructions.'
    )

    program_types: List[ProgramTypeAbridged] = Field(
        default=None,
        description='List of all ProgramTypes in the Model.'
    )

    schedules: List[Union[ScheduleRulesetAbridged, ScheduleFixedIntervalAbridged]] = Field(
        default=None,
        description='A list of all unique schedules in the model. This includes '
            'schedules across all ProgramTypes, Rooms, and Shades.'
    )

    schedule_type_limits: List[ScheduleTypeLimit] = Field(
        default=None,
        description='A list of all unique ScheduleTypeLimits in the model. This '
            'all ScheduleTypeLimits needed to make the Model schedules.'
    )
