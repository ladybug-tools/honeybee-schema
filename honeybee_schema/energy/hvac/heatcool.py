"""Heating/cooling systems without any ventilation."""
from pydantic import Field, constr
from enum import Enum

from ._template import _TemplateSystem


class _HeatCoolBase(_TemplateSystem):
    """Base class for all heating/cooling systems without any ventilation."""


class FCUEquipmentType(str, Enum):
    fcu_chill_gb = 'Fan coil chiller with boiler'
    fcu_chill_ashp = 'Fan coil chiller with central air source heat pump'
    fcu_chill_dhw = 'Fan coil chiller with district hot water'
    fcu_chill_base = 'Fan coil chiller with baseboard electric'
    fcu_chill_guh = 'Fan coil chiller with gas unit heaters'
    fcu_chill = 'Fan coil chiller with no heat'
    fcu_ac_chill_gb = 'Fan coil air-cooled chiller with boiler'
    fcu_ac_chill_ashp = 'Fan coil air-cooled chiller with central air source heat pump'
    fcu_ac_chill_dhw = 'Fan coil air-cooled chiller with district hot water'
    fcu_ac_chill_base = 'Fan coil air-cooled chiller with baseboard electric'
    fcu_ac_chill_guh = 'Fan coil air-cooled chiller with gas unit heaters'
    fcu_ac_chill = 'Fan coil air-cooled chiller with no heat'
    fcu_dcw_gb = 'Fan coil district chilled water with boiler'
    fcu_dcw_ashp = 'Fan coil district chilled water with central air source heat pump'
    fcu_dcw_dhw = 'Fan coil district chilled water with district hot water'
    fcu_dcw_base = 'Fan coil district chilled water with baseboard electric'
    fcu_dcw_guh = 'Fan coil district chilled water with gas unit heaters'
    fcu_dcw = 'Fan coil district chilled water with no heat'


class BaseboardEquipmentType(str, Enum):
    e_base = 'Baseboard electric'
    gb_base = 'Baseboard gas boiler'
    ashp_base = 'Baseboard central air source heat pump'
    dhw_base = 'Baseboard district hot water'


class EvaporativeCoolerEquipmentType(str, Enum):
    evap_e_base = 'Direct evap coolers with baseboard electric'
    evap_gb_base = 'Direct evap coolers with baseboard gas boiler'
    evap_ashp_base = 'Direct evap coolers with baseboard central air source heat pump'
    evap_dhw_base = 'Direct evap coolers with baseboard district hot water'
    evap_furnace = 'Direct evap coolers with forced air furnace'
    evap_guh = 'Direct evap coolers with gas unit heaters'
    evap = 'Direct evap coolers with no heat'


class WSHPEquipmentType(str, Enum):
    wshp_fc_gb = 'Water source heat pumps fluid cooler with boiler'
    wshp_ct_gb = 'Water source heat pumps cooling tower with boiler'
    wshp_gshp = 'Water source heat pumps with ground source heat pump'
    wshp_dcw_dhw = 'Water source heat pumps district chilled water with district hot water'


class ResidentialEquipmentType(str, Enum):
    res_ac_e_base = 'Residential AC with baseboard electric'
    res_ac_gb_base = 'Residential AC with baseboard gas boiler'
    res_ac_ashp_base = 'Residential AC with baseboard central air source heat pump'
    res_ac_dhw_base = 'Residential AC with baseboard district hot water'
    res_ac_furnace = 'Residential AC with residential forced air furnace'
    res_ac = 'Residential AC with no heat'
    res_hp = 'Residential heat pump'
    res_hp_no_cool = 'Residential heat pump with no cooling'
    res_furnace = 'Residential forced air furnace'


class WindowACEquipmentType(str, Enum):
    win_ac_e_base = 'Window AC with baseboard electric'
    win_ac_gb_base = 'Window AC with baseboard gas boiler'
    win_ac_ashp_base = 'Window AC with baseboard central air source heat pump'
    win_ac_dhw_base = 'Window AC with baseboard district hot water'
    win_ac_furnace = 'Window AC with forced air furnace'
    win_ac_guh = 'Window AC with unit heaters'
    win_ac = 'Window AC with no heat'


class VRFEquipmentType(str, Enum):
    vrf = 'VRF'


class GasUnitHeaterEquipmentType(str, Enum):
    guh = 'Gas unit heaters'


class FCU(_HeatCoolBase):
    """Fan Coil Unit (FCU) heating/cooling system (with no ventilation)."""

    type: constr(regex='^FCU$') = 'FCU'

    equipment_type: FCUEquipmentType = Field(
        FCUEquipmentType.fcu_chill_gb,
        description='Text for the specific type of system equipment from the '
        'FCUEquipmentType enumeration.'
    )


class Baseboard(_HeatCoolBase):
    """Baseboard heating system. Intended for spaces only requiring heating."""

    type: constr(regex='^Baseboard$') = 'Baseboard'

    equipment_type: BaseboardEquipmentType = Field(
        BaseboardEquipmentType.e_base,
        description='Text for the specific type of system equipment from the '
        'BaseboardEquipmentType enumeration.'
    )


class EvaporativeCooler(_HeatCoolBase):
    """Direct evaporative cooling systems (with optional heating)."""

    type: constr(regex='^EvaporativeCooler$') = 'EvaporativeCooler'

    equipment_type: EvaporativeCoolerEquipmentType = Field(
        EvaporativeCoolerEquipmentType.evap_e_base,
        description='Text for the specific type of system equipment from the '
        'EvaporativeCoolerEquipmentType enumeration.'
    )


class WSHP(_HeatCoolBase):
    """Direct evaporative cooling systems (with optional heating)."""

    type: constr(regex='^WSHP$') = 'WSHP'

    equipment_type: WSHPEquipmentType = Field(
        WSHPEquipmentType.wshp_fc_gb,
        description='Text for the specific type of system equipment from the '
        'WSHPEquipmentType enumeration.'
    )


class Residential(_HeatCoolBase):
    """Residential Air Conditioning, Heat Pump or Furnace system."""

    type: constr(regex='^Residential$') = 'Residential'

    equipment_type: ResidentialEquipmentType = Field(
        ResidentialEquipmentType.res_ac_e_base,
        description='Text for the specific type of system equipment from the '
        'ResidentialEquipmentType enumeration.'
    )


class WindowAC(_HeatCoolBase):
    """Window Air Conditioning cooling system (with optional heating)."""

    type: constr(regex='^WindowAC$') = 'WindowAC'

    equipment_type: WindowACEquipmentType = Field(
        WindowACEquipmentType.win_ac_e_base,
        description='Text for the specific type of system equipment from the '
        'WindowACEquipmentType enumeration.'
    )


class VRF(_HeatCoolBase):
    """Variable Refrigerant Flow (VRF) heating/cooling system (with no ventilation)."""

    type: constr(regex='^VRF$') = 'VRF'

    equipment_type: VRFEquipmentType = Field(
        VRFEquipmentType.vrf,
        description='Text for the specific type of system equipment from the '
        'VRFEquipmentType enumeration.'
    )


class GasUnitHeater(_HeatCoolBase):
    """Gas unit heating system. Intended for spaces only requiring heating."""

    type: constr(regex='^GasUnitHeater$') = 'GasUnitHeater'

    equipment_type: GasUnitHeaterEquipmentType = Field(
        GasUnitHeaterEquipmentType.guh,
        description='Text for the specific type of system equipment from the '
        'GasUnitHeaterEquipmentType enumeration.'
    )
