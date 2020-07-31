"""HVAC systems with DOAS, separating ventilation and meeting thermal demand."""
from pydantic import Field, constr
from typing import Union
from enum import Enum

from ._template import _TemplateSystem
from ...altnumber import Autosize


class _DOASBase(_TemplateSystem):
    """Base class for DOAS systems."""

    sensible_heat_recovery: Union[Autosize, float] = Field(
        Autosize(),
        ge=0,
        le=1,
        description='A number between 0 and 1 for the effectiveness of sensible '
        'heat recovery within the system. If None or Autosize, it will be whatever '
        'is recommended for the given vintage.'
    )

    latent_heat_recovery: Union[Autosize, float] = Field(
        Autosize(),
        ge=0,
        le=1,
        description='A number between 0 and 1 for the effectiveness of latent '
        'heat recovery within the system. If None or Autosize, it will be whatever '
        'is recommended for the given vintage.'
    )


class FCUwithDOASEquipmentType(str, Enum):
    fcu_chill_gb = 'DOAS with fan coil chiller with boiler'
    fcu_chill_ashp = 'DOAS with fan coil chiller with central air source heat pump'
    fcu_chill_dhw = 'DOAS with fan coil chiller with district hot water'
    fcu_chill_base = 'DOAS with fan coil chiller with baseboard electric'
    fcu_chill_guh = 'DOAS with fan coil chiller with gas unit heaters'
    fcu_chill = 'DOAS with fan coil chiller with no heat'
    fcu_ac_chill_gb = 'DOAS with fan coil air-cooled chiller with boiler'
    fcu_ac_chill_ashp = 'DOAS with fan coil air-cooled chiller with central air source heat pump'
    fcu_ac_chill_dhw = 'DOAS with fan coil air-cooled chiller with district hot water'
    fcu_ac_chill_base = 'DOAS with fan coil air-cooled chiller with baseboard electric'
    fcu_ac_chill_guh = 'DOAS with fan coil air-cooled chiller with gas unit heaters'
    fcu_ac_chill = 'DOAS with fan coil air-cooled chiller with no heat'
    fcu_dcw_gb = 'DOAS with fan coil district chilled water with boiler'
    fcu_dcw_ashp = 'DOAS with fan coil district chilled water with central air source heat pump'
    fcu_dcw_dhw = 'DOAS with fan coil district chilled water with district hot water'
    fcu_dcw_base = 'DOAS with fan coil district chilled water with baseboard electric'
    fcu_dcw_guh = 'DOAS with fan coil district chilled water with gas unit heaters'
    fcu_dcw = 'DOAS with fan coil district chilled water with no heat'


class WSHPwithDOASEquipmentType(str, Enum):
    wshp_fc_gb = 'DOAS with water source heat pumps fluid cooler with boiler'
    wshp_ct_gb = 'DOAS with water source heat pumps cooling tower with boiler'
    wshp_gshp = 'DOAS with water source heat pumps with ground source heat pump'
    wshp_dcw_dhw = 'DOAS with water source heat pumps district chilled water with district hot water'


class VRFwithDOASEquipmentType(str, Enum):
    vrf = 'DOAS with VRF'


class FCUwithDOAS(_DOASBase):
    """Fan Coil Unit (FCU) with DOAS HVAC system."""

    type: constr(regex='^FCUwithDOAS$') = 'FCUwithDOAS'

    equipment_type: FCUwithDOASEquipmentType = Field(
        FCUwithDOASEquipmentType.fcu_chill_gb,
        description='Text for the specific type of system equipment from the '
        'FCUwithDOASEquipmentType enumeration.'
    )


class WSHPwithDOAS(_DOASBase):
    """Water Source Heat Pump (WSHP) with DOAS HVAC system."""

    type: constr(regex='^WSHPwithDOAS$') = 'WSHPwithDOAS'

    equipment_type: WSHPwithDOASEquipmentType = Field(
        WSHPwithDOASEquipmentType.wshp_fc_gb,
        description='Text for the specific type of system equipment from the '
        'WSHPwithDOASEquipmentType enumeration.'
    )


class VRFwithDOAS(_DOASBase):
    """Variable Refrigerant Flow (VRF) with DOAS HVAC system."""

    type: constr(regex='^VRFwithDOAS$') = 'VRFwithDOAS'

    equipment_type: VRFwithDOASEquipmentType = Field(
        VRFwithDOASEquipmentType.vrf,
        description='Text for the specific type of system equipment from the '
        'VRFwithDOASEquipmentType enumeration.'
    )
