"""HVAC systems with DOAS, separating ventilation and meeting thermal demand."""
from pydantic import Field, constr
from typing import Union
from enum import Enum

from ._template import _TemplateSystem


class _DOASBase(_TemplateSystem):
    """Base class for DOAS systems."""

    sensible_heat_recovery: float = Field(
        0,
        ge=0,
        le=1,
        description='A number between 0 and 1 for the effectiveness of sensible '
        'heat recovery within the system.'
    )

    latent_heat_recovery: float = Field(
        0,
        ge=0,
        le=1,
        description='A number between 0 and 1 for the effectiveness of latent '
        'heat recovery within the system.'
    )

    demand_controlled_ventilation: bool = Field(
        False,
        description='Boolean to note whether demand controlled ventilation should be '
        'used on the system, which will vary the amount of ventilation air according '
        'to the occupancy schedule of the Rooms.'
    )

    doas_availability_schedule: str = Field(
        None,
        min_length=1,
        max_length=100,
        description='An optional On/Off discrete schedule to set when the dedicated '
        'outdoor air system (DOAS) shuts off. This will not only prevent any outdoor '
        'air from flowing thorough the system but will also shut off the fans, which '
        'can result in more energy savings when spaces served by the DOAS are '
        'completely unoccupied. If None, the DOAS will be always on.'
    )


class FCUwithDOASEquipmentType(str, Enum):
    fcu_chill_gb = 'DOAS_FCU_Chiller_Boiler'
    fcu_chill_ashp = 'DOAS_FCU_Chiller_ASHP'
    fcu_chill_dhw = 'DOAS_FCU_Chiller_DHW'
    fcu_chill_base = 'DOAS_FCU_Chiller_ElectricBaseboard'
    fcu_chill_guh = 'DOAS_FCU_Chiller_GasHeaters'
    fcu_chill = 'DOAS_FCU_Chiller'
    fcu_ac_chill_gb = 'DOAS_FCU_ACChiller_Boiler'
    fcu_ac_chill_ashp = 'DOAS_FCU_ACChiller_ASHP'
    fcu_ac_chill_dhw = 'DOAS_FCU_ACChiller_DHW'
    fcu_ac_chill_base = 'DOAS_FCU_ACChiller_ElectricBaseboard'
    fcu_ac_chill_guh = 'DOAS_FCU_ACChiller_GasHeaters'
    fcu_ac_chill = 'DOAS_FCU_ACChiller'
    fcu_dcw_gb = 'DOAS_FCU_DCW_Boiler'
    fcu_dcw_ashp = 'DOAS_FCU_DCW_ASHP'
    fcu_dcw_dhw = 'DOAS_FCU_DCW_DHW'
    fcu_dcw_base = 'DOAS_FCU_DCW_ElectricBaseboard'
    fcu_dcw_guh = 'DOAS_FCU_DCW_GasHeaters'
    fcu_dcw = 'DOAS_FCU_DCW'


class WSHPwithDOASEquipmentType(str, Enum):
    wshp_fc_gb = 'DOAS_WSHP_FluidCooler_Boiler'
    wshp_ct_gb = 'DOAS_WSHP_CoolingTower_Boiler'
    wshp_gshp = 'DOAS_WSHP_GSHP'
    wshp_dcw_dhw = 'DOAS_WSHP_DCW_DHW'


class VRFwithDOASEquipmentType(str, Enum):
    vrf = 'DOAS_VRF'


class FCUwithDOASAbridged(_DOASBase):
    """Fan Coil Unit (FCU) with DOAS HVAC system."""

    type: constr(regex='^FCUwithDOASAbridged$') = 'FCUwithDOASAbridged'

    equipment_type: FCUwithDOASEquipmentType = Field(
        FCUwithDOASEquipmentType.fcu_chill_gb,
        description='Text for the specific type of system equipment from the '
        'FCUwithDOASEquipmentType enumeration.'
    )


class WSHPwithDOASAbridged(_DOASBase):
    """Water Source Heat Pump (WSHP) with DOAS HVAC system."""

    type: constr(regex='^WSHPwithDOASAbridged$') = 'WSHPwithDOASAbridged'

    equipment_type: WSHPwithDOASEquipmentType = Field(
        WSHPwithDOASEquipmentType.wshp_fc_gb,
        description='Text for the specific type of system equipment from the '
        'WSHPwithDOASEquipmentType enumeration.'
    )


class VRFwithDOASAbridged(_DOASBase):
    """Variable Refrigerant Flow (VRF) with DOAS HVAC system."""

    type: constr(regex='^VRFwithDOASAbridged$') = 'VRFwithDOASAbridged'

    equipment_type: VRFwithDOASEquipmentType = Field(
        VRFwithDOASEquipmentType.vrf,
        description='Text for the specific type of system equipment from the '
        'VRFwithDOASEquipmentType enumeration.'
    )