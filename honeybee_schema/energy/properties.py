"""Model energy properties."""
from pydantic import Field, constr
from typing import List, Union

from .._base import NoExtraBaseModel
from .constructionset import ConstructionSetAbridged, ConstructionSet
from .global_constructionset import GlobalConstructionSet
from .construction import OpaqueConstructionAbridged, WindowConstructionAbridged, \
    ShadeConstruction, AirBoundaryConstructionAbridged, OpaqueConstruction, \
    WindowConstruction, AirBoundaryConstruction, WindowConstructionShadeAbridged, \
    WindowConstructionShade, WindowConstructionDynamicAbridged, WindowConstructionDynamic
from .material import EnergyMaterial, EnergyMaterialNoMass, EnergyMaterialVegetation, \
    EnergyWindowMaterialSimpleGlazSys, EnergyWindowMaterialGlazing, \
    EnergyWindowMaterialGas, EnergyWindowMaterialGasCustom, \
    EnergyWindowMaterialGasMixture, EnergyWindowFrame, \
    EnergyWindowMaterialBlind, EnergyWindowMaterialShade
from .programtype import ProgramTypeAbridged, ProgramType
from .load import PeopleAbridged, LightingAbridged, ElectricEquipmentAbridged, \
    GasEquipmentAbridged, ServiceHotWaterAbridged, InfiltrationAbridged, \
    VentilationAbridged, SetpointAbridged, ProcessAbridged
from .daylight import DaylightingControl
from .ventcool import VentilationControlAbridged, VentilationOpening, \
    VentilationSimulationControl, AFNCrack
from .internalmass import InternalMassAbridged
from .schedule import ScheduleTypeLimit, ScheduleRulesetAbridged, \
    ScheduleFixedIntervalAbridged, ScheduleRuleset, ScheduleFixedInterval
from .hvac.idealair import IdealAirSystemAbridged
from .hvac.allair import VAV, PVAV, PSZ, PTAC, ForcedAirFurnace
from .hvac.doas import FCUwithDOASAbridged, WSHPwithDOASAbridged, VRFwithDOASAbridged, \
    RadiantwithDOASAbridged
from .hvac.heatcool import FCU, WSHP, VRF, Baseboard, EvaporativeCooler, Residential, \
    WindowAC, GasUnitHeater, Radiant
from .shw import SHWSystem


class ShadeEnergyPropertiesAbridged(NoExtraBaseModel):

    type: constr(regex='^ShadeEnergyPropertiesAbridged$') = \
        'ShadeEnergyPropertiesAbridged'

    construction: str = Field(
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
        'be completely opaque.'
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

    vent_opening: VentilationOpening = Field(
        default=None,
        description='An optional VentilationOpening to specify the operable '
        'portion of the Door.'
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

    vent_opening: VentilationOpening = Field(
        default=None,
        description='An optional VentilationOpening to specify the operable '
        'portion of the Aperture.'
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

    vent_crack: AFNCrack = Field(
        default=None,
        description='An optional AFNCrack to specify airflow through a surface crack '
        'used by the AirflowNetwork.'
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

    shw: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='An optional identifier of a Service Hot Water (SHW) system '
        'that specifies how the hot water load of the Room is met. If None, the hot '
        'water load will be met with a generic system that only measures thermal load'
        'and does not account for system efficiencies.'
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

    service_hot_water: ServiceHotWaterAbridged = Field(
        default=None,
        description='ServiceHotWater object to describe the hot water usage.'
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

    daylighting_control: DaylightingControl = Field(
        default=None,
        description='An optional DaylightingControl object to dictate the dimming '
        'of lights. If None, the lighting will respond only to the schedule and '
        'not the daylight conditions within the room.'
    )

    window_vent_control: VentilationControlAbridged = Field(
        default=None,
        description='An optional VentilationControl object to dictate the opening '
        'of windows. If None, the windows will never open.'
    )

    internal_masses: List[InternalMassAbridged] = Field(
        default=None,
        description='An optional list of of InternalMass objects for thermal mass '
        'exposed to Room air. Note that internal masses assigned this way cannot "see" '
        'solar radiation that may potentially hit them and, as such, caution should be '
        'taken when using this component with internal mass objects that are not '
        'always in shade. Masses are factored into the the thermal calculations '
        'of the Room by undergoing heat transfer with the indoor air.'
    )

    process_loads: List[ProcessAbridged] = Field(
        default=None,
        description='An optional list of of Process objects for process loads within '
        'the room. These can represent kilns, manufacturing equipment, and various '
        'industrial processes. They can also be used to represent wood burning '
        'fireplaces or certain pieces of equipment to be separated from the other '
        'end uses.'
    )


class ModelEnergyProperties(NoExtraBaseModel):

    type: constr(regex='^ModelEnergyProperties$') = \
        'ModelEnergyProperties'

    global_construction_set: GlobalConstructionSet = Field(
        default=GlobalConstructionSet(),
        description='Global Energy construction set.',
        readOnly=True
    )

    construction_sets: List[Union[ConstructionSetAbridged, ConstructionSet]] = Field(
        default=None,
        description='List of all unique ConstructionSets in the Model.'
    )

    constructions: List[
        Union[
            OpaqueConstructionAbridged, WindowConstructionAbridged,
            WindowConstructionShadeAbridged, AirBoundaryConstructionAbridged,
            OpaqueConstruction, WindowConstruction, WindowConstructionShade,
            WindowConstructionDynamicAbridged, WindowConstructionDynamic,
            AirBoundaryConstruction, ShadeConstruction
        ]
    ] = Field(
        default=None,
        description='A list of all unique constructions in the model. This includes '
        'constructions across all Faces, Apertures, Doors, Shades, Room '
        'ConstructionSets, and the global_construction_set.'
    )

    materials: List[
        Union[
            EnergyMaterial, EnergyMaterialNoMass, EnergyMaterialVegetation,
            EnergyWindowMaterialGlazing, EnergyWindowMaterialSimpleGlazSys,
            EnergyWindowMaterialGas, EnergyWindowMaterialGasMixture,
            EnergyWindowMaterialGasCustom, EnergyWindowFrame,
            EnergyWindowMaterialBlind, EnergyWindowMaterialShade
        ]
    ] = Field(
        default=None,
        description='A list of all unique materials in the model. This includes '
        'materials needed to make the Model constructions.'
    )

    hvacs: List[
        Union[
            IdealAirSystemAbridged, VAV, PVAV, PSZ, PTAC, ForcedAirFurnace,
            FCUwithDOASAbridged, WSHPwithDOASAbridged, VRFwithDOASAbridged,
            RadiantwithDOASAbridged,
            FCU, WSHP, VRF, Baseboard, EvaporativeCooler, Residential,
            WindowAC, GasUnitHeater, Radiant
        ]
    ] = Field(
        default=None,
        description='List of all unique HVAC systems in the Model.'
    )

    shws: List[SHWSystem] = Field(
        default=None,
        description='List of all unique Service Hot Water (SHW) systems in the Model.'
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

    ventilation_simulation_control: VentilationSimulationControl = Field(
        default=None,
        description='An optional parameter to define the global parameters for '
        'a ventilation cooling.'
    )
