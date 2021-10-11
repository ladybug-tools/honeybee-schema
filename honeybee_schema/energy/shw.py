"""Ideal Air Schema"""
from pydantic import Field, constr, confloat
from typing import Union
from enum import Enum

from ._base import IDdEnergyBaseModel
from ..altnumber import Autocalculate


class SHWEquipmentType(str, Enum):
    gas_waterheater = 'Gas_WaterHeater'
    electric_waterheater = 'Electric_WaterHeater'
    heatpump_waterheater = 'HeatPump_WaterHeater'
    gas_tanklessheater = 'Gas_TanklessHeater'
    electric_tanklessheater = 'Electric_TanklessHeater'


class SHWSystem(IDdEnergyBaseModel):
    """Provides a model for a Service Hot Water system."""

    type: constr(regex='^SHWSystem$') = 'SHWSystem'

    equipment_type: SHWEquipmentType = Field(
        SHWEquipmentType.gas_waterheater,
        description='Text to indicate the type of air-side economizer used on the '
        'ideal air system. Economizers will mix in a greater amount of outdoor '
        'air to cool the zone (rather than running the cooling system) when '
        'the zone needs cooling and the outdoor air is cooler than the zone.'
    )

    heater_efficiency: Union[confloat(gt=0), Autocalculate] = Field(
        Autocalculate(),
        description='A number for the efficiency of the heater within the system. '
        'For Gas systems, this is the efficiency of the burner. For HeatPump '
        'systems, this is the rated COP of the system. For electric systems, this '
        'should usually be set to 1. If set to Autocalculate, this value will '
        'automatically be set based on the equipment_type. Gas_WaterHeater - 0.8, '
        'Electric_WaterHeater - 1.0, HeatPump_WaterHeater - 3.5, Gas_TanklessHeater '
        '- 0.8, Electric_TanklessHeater - 1.0.'
    )

    ambient_condition: Union[float, str] = Field(
        22,
        description='A number for the ambient temperature in which the hot '
        'water tank is located [C]. This can also be the identifier of a Room '
        'in which the tank is located.'
    )

    ambient_loss_coefficient: float = Field(
        6,
        description='A number for the loss of heat from the water heater '
        'tank to the surrounding ambient conditions [W/K].'
    )
