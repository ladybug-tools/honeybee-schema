"""Model energy properties."""
from pydantic import Field, constr
from typing import List, Union
from enum import Enum

from .._base import NoExtraBaseModel
from .constructionset import ConstructionSetAbridged, ConstructionSet
from .construction import OpaqueConstructionAbridged, WindowConstructionAbridged, \
    ShadeConstruction, AirBoundaryConstructionAbridged, OpaqueConstruction, \
    WindowConstruction, AirBoundaryConstruction
from .material import EnergyMaterial, EnergyMaterialNoMass, \
    EnergyWindowMaterialGas, EnergyWindowMaterialGasCustom, \
    EnergyWindowMaterialGasMixture, EnergyWindowMaterialSimpleGlazSys, \
    EnergyWindowMaterialBlind, EnergyWindowMaterialGlazing, EnergyWindowMaterialShade
from .programtype import ProgramTypeAbridged, ProgramType
from .load import PeopleAbridged, LightingAbridged, ElectricEquipmentAbridged, \
    GasEquipmentAbridged, InfiltrationAbridged, VentilationAbridged, SetpointAbridged
from .schedule import ScheduleTypeLimit, ScheduleRulesetAbridged, \
    ScheduleFixedIntervalAbridged, ScheduleRuleset, ScheduleFixedInterval
from .hvac import IdealAirSystemAbridged


class ShadeEnergyPropertiesAbridged(NoExtraBaseModel):

    type: constr(regex='^ShadeEnergyPropertiesAbridged$') = \
        'ShadeEnergyPropertiesAbridged'

    construction:  str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier of a ShadeConstruction to set the reflectance and '
            'specularity of the Shade. If None, the construction is set by the'
            'parent Room construction_set, the Model global_construction_set or '
            '(in the case fo an orphaned shade) the EnergyPlus default of 0.2 '
            'diffuse reflectance.'
    )

    transmittance_schedule: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier of a schedule to set the transmittance of the shade, '
            'which can vary throughout the simulation. If None, the shade will '
            'be completely opauqe.'
    )


class DoorEnergyPropertiesAbridged(NoExtraBaseModel):

    type: constr(regex='^DoorEnergyPropertiesAbridged$') = \
        'DoorEnergyPropertiesAbridged'

    construction: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier of an OpaqueConstruction or WindowConstruction '
            'for the door. Note that the host door must have the is_glass property '
            'set to True to assign a WindowConstruction. If None, the construction '
            'is set by the parent Room construction_set or the Model '
            'global_construction_set.'
    )


class ApertureEnergyPropertiesAbridged(NoExtraBaseModel):

    type: constr(regex='^ApertureEnergyPropertiesAbridged$') = \
        'ApertureEnergyPropertiesAbridged'

    construction: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier of a WindowConstruction for the aperture. If None, the '
            'construction is set by the parent Room construction_set or the Model '
            'global_construction_set.'
    )


class FaceEnergyPropertiesAbridged(NoExtraBaseModel):

    type: constr(regex='^FaceEnergyPropertiesAbridged$') = \
        'FaceEnergyPropertiesAbridged'

    construction: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier of an OpaqueConstruction for the Face. If None, the '
            'construction is set by the parent Room construction_set or the '
            'Model global_construction_set.'
    )


class RoomEnergyPropertiesAbridged(NoExtraBaseModel):

    type: constr(regex='^RoomEnergyPropertiesAbridged$') = \
        'RoomEnergyPropertiesAbridged'

    construction_set: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier of a ConstructionSet to specify all default '
            'constructions for the Faces, Apertures, and Doors of the Room. If '
            'None, the Room will use the Model global_construction_set.'
    )

    program_type: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier of a ProgramType to specify all default schedules '
            'and loads for the Room. If None, the Room will have no loads or setpoints.'
    )

    hvac: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='An optional identifier of a HVAC system (such as an IdealAirSystem)'
            ' that specifies how the Room is conditioned. If None, it will be assumed '
            'that the Room is not conditioned.'
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
        description='ElectricEquipment object to describe the electric equipment usage.'
    )

    gas_equipment: GasEquipmentAbridged = Field(
        default=None,
        description='GasEquipment object to describe the gas equipment usage.'
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


class ModelEnergyProperties(NoExtraBaseModel):

    type: constr(regex='^ModelEnergyProperties$') = \
        'ModelEnergyProperties'

    terrain_type: TerrianTypes = Field(
        default=TerrianTypes.city,
        description='Text for the terrain in which the model sits. This is used '
            'to determine the wind profile over the height of the rooms.'
    )

    global_construction_set: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Identifier for the ConstructionSet to be used for all '
            'objects lacking their own construction or a parent Room construction_set. '
            'This ConstructionSet must appear under the Model construction_sets.'
    )

    construction_sets: List[Union[ConstructionSetAbridged, ConstructionSet]] = Field(
        default=None,
        description='List of all unique ConstructionSets in the Model.'
    )

    constructions: List[Union[
        OpaqueConstructionAbridged, WindowConstructionAbridged,
        ShadeConstruction, AirBoundaryConstructionAbridged,
        OpaqueConstruction, WindowConstruction, AirBoundaryConstruction]] = Field(
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

    hvacs: List[Union[IdealAirSystemAbridged]] = Field(
        default=None,
        description='List of all unique HVAC systems in the Model.'
    )

    program_types: List[Union[ProgramTypeAbridged, ProgramType]] = Field(
        default=None,
        description='List of all unique ProgramTypes in the Model.'
    )

    schedules: List[Union[ScheduleRulesetAbridged, ScheduleFixedIntervalAbridged,
                          ScheduleRuleset, ScheduleFixedInterval]] = Field(
        default=None,
        description='A list of all unique schedules in the model. This includes '
            'schedules across all HVAC systems, ProgramTypes, Rooms, and Shades.'
    )

    schedule_type_limits: List[ScheduleTypeLimit] = Field(
        default=None,
        description='A list of all unique ScheduleTypeLimits in the model. This '
            'all ScheduleTypeLimits needed to make the Model schedules.'
    )
