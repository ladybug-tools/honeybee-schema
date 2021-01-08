"""Heating/cooling systems without any ventilation."""
from pydantic import Field, constr
from enum import Enum

from ._template import _TemplateSystem


class _HeatCoolBase(_TemplateSystem):
    """Base class for all heating/cooling systems without any ventilation."""


class FCUEquipmentType(str, Enum):
    fcu_chill_gb = 'FCU_Chiller_Boiler'
    fcu_chill_ashp = 'FCU_Chiller_ASHP'
    fcu_chill_dhw = 'FCU_Chiller_DHW'
    fcu_chill_base = 'FCU_Chiller_ElectricBaseboard'
    fcu_chill_guh = 'FCU_Chiller_GasHeaters'
    fcu_chill = 'FCU_Chiller'
    fcu_ac_chill_gb = 'FCU_ACChiller_Boiler'
    fcu_ac_chill_ashp = 'FCU_ACChiller_ASHP'
    fcu_ac_chill_dhw = 'FCU_ACChiller_DHW'
    fcu_ac_chill_base = 'FCU_ACChiller_ElectricBaseboard'
    fcu_ac_chill_guh = 'FCU_ACChiller_GasHeaters'
    fcu_ac_chill = 'FCU_ACChiller'
    fcu_dcw_gb = 'FCU_DCW_Boiler'
    fcu_dcw_ashp = 'FCU_DCW_ASHP'
    fcu_dcw_dhw = 'FCU_DCW_DHW'
    fcu_dcw_base = 'FCU_DCW_ElectricBaseboard'
    fcu_dcw_guh = 'FCU_DCW_GasHeaters'
    fcu_dcw = 'FCU_DCW'


class BaseboardEquipmentType(str, Enum):
    e_base = 'ElectricBaseboard'
    gb_base = 'BoilerBaseboard'
    ashp_base = 'ASHPBaseboard'
    dhw_base = 'DHWBaseboard'


class EvaporativeCoolerEquipmentType(str, Enum):
    evap_e_base = 'EvapCoolers_ElectricBaseboard'
    evap_gb_base = 'EvapCoolers_BoilerBaseboard'
    evap_ashp_base = 'EvapCoolers_ASHPBaseboard'
    evap_dhw_base = 'EvapCoolers_DHWBaseboard'
    evap_furnace = 'EvapCoolers_Furnace'
    evap_guh = 'EvapCoolers_UnitHeaters'
    evap = 'EvapCoolers'


class WSHPEquipmentType(str, Enum):
    wshp_fc_gb = 'WSHP_FluidCooler_Boiler'
    wshp_ct_gb = 'WSHP_CoolingTower_Boiler'
    wshp_gshp = 'WSHP_GSHP'
    wshp_dcw_dhw = 'WSHP_DCW_DHW'


class ResidentialEquipmentType(str, Enum):
    res_ac_e_base = 'ResidentialAC_ElectricBaseboard'
    res_ac_gb_base = 'ResidentialAC_BoilerBaseboard'
    res_ac_ashp_base = 'ResidentialAC_ASHPBaseboard'
    res_ac_dhw_base = 'ResidentialAC_DHWBaseboard'
    res_ac_furnace = 'ResidentialAC_ResidentialFurnace'
    res_ac = 'ResidentialAC'
    res_hp = 'ResidentialHP'
    res_hp_no_cool = 'ResidentialHPNoCool'
    res_furnace = 'ResidentialFurnace'


class WindowACEquipmentType(str, Enum):
    win_ac_e_base = 'WindowAC_ElectricBaseboard'
    win_ac_gb_base = 'WindowAC_BoilerBaseboard'
    win_ac_ashp_base = 'WindowAC_ASHPBaseboard'
    win_ac_dhw_base = 'WindowAC_DHWBaseboard'
    win_ac_furnace = 'WindowAC_Furnace'
    win_ac_guh = 'WindowAC_GasHeaters'
    win_ac = 'WindowAC'


class VRFEquipmentType(str, Enum):
    vrf = 'VRF'


class GasUnitHeaterEquipmentType(str, Enum):
    guh = 'GasHeaters'


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
