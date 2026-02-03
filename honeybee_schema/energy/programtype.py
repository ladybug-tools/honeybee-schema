"""Programtype Schema"""
from pydantic import Field
from typing import List, Union

from ._base import IDdEnergyBaseModel
from .load import PeopleAbridged, LightingAbridged, ElectricEquipmentAbridged, \
    GasEquipmentAbridged, ServiceHotWaterAbridged, \
    InfiltrationAbridged, VentilationAbridged, SetpointAbridged, ProcessAbridged, People, Lighting, ElectricEquipment, GasEquipment, ServiceHotWater, \
    Infiltration, Ventilation, Setpoint
from typing import Literal


class ProgramTypeAbridged(IDdEnergyBaseModel):

    type: Literal['ProgramTypeAbridged'] = 'ProgramTypeAbridged'

    people: Union[PeopleAbridged, None] = Field(
        default=None,
        description='People to describe the occupancy of the program. If None, '
        'no occupancy will be assumed for the program.'
    )

    lighting: Union[LightingAbridged, None] = Field(
        default=None,
        description='Lighting to describe the lighting usage of the program. '
        'If None, no lighting will be assumed for the program.'
    )

    electric_equipment: Union[ElectricEquipmentAbridged, None] = Field(
        default=None,
        description='ElectricEquipment to describe the usage of electric equipment '
        'within the program. If None, no electric equipment will be assumed.'
    )

    gas_equipment: Union[GasEquipmentAbridged, None] = Field(
        default=None,
        description='GasEquipment to describe the usage of gas equipment '
        'within the program. If None, no gas equipment will be assumed.'
    )

    service_hot_water: Union[ServiceHotWaterAbridged, None] = Field(
        default=None,
        description='ServiceHotWater object to describe the usage of hot water '
        'within the program. If None, no hot water will be assumed.'
    )

    infiltration: Union[InfiltrationAbridged, None] = Field(
        default=None,
        description='Infiltration to describe the outdoor air leakage of '
        'the program. If None, no infiltration will be assumed for the program.'
    )

    ventilation: Union[VentilationAbridged, None] = Field(
        default=None,
        description='Ventilation to describe the minimum outdoor air requirement '
        'of the program. If None, no ventilation requirement will be assumed.'
    )

    setpoint: Union[SetpointAbridged, None] = Field(
        default=None,
        description='Setpoint object to describe the temperature and humidity setpoints '
        'of the program.  If None, the ProgramType cannot be assigned to a Room '
        'that is conditioned.'
    )

    process_loads: Union[List[ProcessAbridged], None] = Field(
        default=None,
        description='A list of Process objects for process loads within the program.'
    )


class ProgramType(ProgramTypeAbridged):

    type: Literal['ProgramType'] = 'ProgramType'

    people: Union[People, None] = Field(
        default=None,
        description='People to describe the occupancy of the program. If None, '
        'no occupancy will be assumed for the program.'
    )

    lighting: Union[Lighting, None] = Field(
        default=None,
        description='Lighting to describe the lighting usage of the program. '
        'If None, no lighting will be assumed for the program.'
    )

    electric_equipment: Union[ElectricEquipment, None] = Field(
        default=None,
        description='ElectricEquipment to describe the usage of electric equipment '
        'within the program. If None, no electric equipment will be assumed.'
    )

    gas_equipment: Union[GasEquipment, None] = Field(
        default=None,
        description='GasEquipment to describe the usage of gas equipment '
        'within the program. If None, no gas equipment will be assumed.'
    )

    service_hot_water: Union[ServiceHotWater, None] = Field(
        default=None,
        description='ServiceHotWater object to describe the usage of hot water '
        'within the program. If None, no hot water will be assumed.'
    )

    infiltration: Union[Infiltration, None] = Field(
        default=None,
        description='Infiltration to describe the outdoor air leakage of '
        'the program. If None, no infiltration will be assumed for the program.'
    )

    ventilation: Union[Ventilation, None] = Field(
        default=None,
        description='Ventilation to describe the minimum outdoor air requirement '
        'of the program. If None, no ventilation requirement will be assumed.'
    )

    setpoint: Union[Setpoint, None] = Field(
        default=None,
        description='Setpoint object to describe the temperature and humidity setpoints '
        'of the program.  If None, the ProgramType cannot be assigned to a Room '
        'that is conditioned.'
    )
