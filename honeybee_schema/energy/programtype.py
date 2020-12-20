"""Programtype Schema"""
from pydantic import Field, constr

from ._base import IDdEnergyBaseModel
from .load import PeopleAbridged, LightingAbridged, ElectricEquipmentAbridged, \
    GasEquipmentAbridged, ServiceHotWaterAbridged, \
    InfiltrationAbridged, VentilationAbridged, SetpointAbridged, \
    People, Lighting, ElectricEquipment, GasEquipment, ServiceHotWater, \
    Infiltration, Ventilation, Setpoint


class ProgramTypeAbridged(IDdEnergyBaseModel):

    type: constr(regex='^ProgramTypeAbridged$') = 'ProgramTypeAbridged'

    people: PeopleAbridged = Field(
        default=None,
        description='People to describe the occupancy of the program. If None, '
        'no occupancy will be assumed for the program.'
    )

    lighting: LightingAbridged = Field(
        default=None,
        description='Lighting to describe the lighting usage of the program. '
        'If None, no lighting will be assumed for the program.'
    )

    electric_equipment: ElectricEquipmentAbridged = Field(
        default=None,
        description='ElectricEquipment to describe the usage of electric equipment '
        'within the program. If None, no electric equipment will be assumed.'
    )

    gas_equipment: GasEquipmentAbridged = Field(
        default=None,
        description='GasEquipment to describe the usage of gas equipment '
        'within the program. If None, no gas equipment will be assumed.'
    )

    service_hot_water: ServiceHotWaterAbridged = Field(
        default=None,
        description='ServiceHotWater object to describe the usage of hot water '
        'within the program. If None, no hot water will be assumed.'
    )

    infiltration: InfiltrationAbridged = Field(
        default=None,
        description='Infiltration to describe the outdoor air leakage of '
        'the program. If None, no infiltration will be assumed for the program.'
    )

    ventilation: VentilationAbridged = Field(
        default=None,
        description='Ventilation to describe the minimum outdoor air requirement '
        'of the program. If None, no ventilation requirement will be assumed.'
    )

    setpoint: SetpointAbridged = Field(
        default=None,
        description='Setpoint object to describe the temperature and humidity setpoints '
        'of the program.  If None, the ProgramType cannot be assigned to a Room '
        'that is conditioned.'
    )


class ProgramType(ProgramTypeAbridged):

    type: constr(regex='^ProgramType$') = 'ProgramType'

    people: People = Field(
        default=None,
        description='People to describe the occupancy of the program. If None, '
        'no occupancy will be assumed for the program.'
    )

    lighting: Lighting = Field(
        default=None,
        description='Lighting to describe the lighting usage of the program. '
        'If None, no lighting will be assumed for the program.'
    )

    electric_equipment: ElectricEquipment = Field(
        default=None,
        description='ElectricEquipment to describe the usage of electric equipment '
        'within the program. If None, no electric equipment will be assumed.'
    )

    gas_equipment: GasEquipment = Field(
        default=None,
        description='GasEquipment to describe the usage of gas equipment '
        'within the program. If None, no gas equipment will be assumed.'
    )

    service_hot_water: ServiceHotWater = Field(
        default=None,
        description='ServiceHotWater object to describe the usage of hot water '
        'within the program. If None, no hot water will be assumed.'
    )

    infiltration: Infiltration = Field(
        default=None,
        description='Infiltration to describe the outdoor air leakage of '
        'the program. If None, no infiltration will be assumed for the program.'
    )

    ventilation: Ventilation = Field(
        default=None,
        description='Ventilation to describe the minimum outdoor air requirement '
        'of the program. If None, no ventilation requirement will be assumed.'
    )

    setpoint: Setpoint = Field(
        default=None,
        description='Setpoint object to describe the temperature and humidity setpoints '
        'of the program.  If None, the ProgramType cannot be assigned to a Room '
        'that is conditioned.'
    )
