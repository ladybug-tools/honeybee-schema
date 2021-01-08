"""All-air HVAC systems, providing ventilation and meeting thermal demand with air."""
from pydantic import Field, constr
from typing import Union
from enum import Enum

from ._template import _TemplateSystem
from ...altnumber import Autosize


class AllAirEconomizerType(str, Enum):
    inferred = 'Inferred'
    no_economizer = 'NoEconomizer'
    differential_dry_bulb = 'DifferentialDryBulb'
    differential_enthalpy = 'DifferentialEnthalpy'


class _AllAirBase(_TemplateSystem):
    """Base class for all-air systems."""

    economizer_type: AllAirEconomizerType = Field(
        AllAirEconomizerType.inferred,
        description='Text to indicate the type of air-side economizer used on '
        'the system (from the AllAirEconomizerType enumeration). If Inferred, the '
        'economizer will be set to whatever is recommended for the given vintage.'
    )

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


class VAVEquipmentType(str, Enum):
    vav_chill_gbr = 'VAV_Chiller_Boiler'
    vav_chill_ashp = 'VAV_Chiller_ASHP'
    vav_chill_dhw = 'VAV_Chiller_DHW'
    vav_chill_pfp = 'VAV_Chiller_PFP'
    vav_chill_gcr = 'VAV_Chiller_GasCoil'
    vav_ac_chill_gbr = 'VAV_ACChiller_Boiler'
    vav_ac_chill_ashp = 'VAV_ACChiller_ASHP'
    vav_ac_chill_dhw = 'VAV_ACChiller_DHW'
    vav_ac_chill_pfp = 'VAV_ACChiller_PFP'
    vav_ac_chill_gcr = 'VAV_ACChiller_GasCoil'
    vav_dcw_gbr = 'VAV_DCW_Boiler'
    vav_dcw_ashp = 'VAV_DCW_ASHP'
    vav_dcw_dhw = 'VAV_DCW_DHW'
    vav_dcw_pfp = 'VAV_DCW_PFP'
    vav_dcw_gcr = 'VAV_DCW_GasCoil'


class PVAVEquipmentType(str, Enum):
    pvav_gbr = 'PVAV_Boiler'
    pvav_ashp = 'PVAV_ASHP'
    pvav_dhw = 'PVAV_DHW'
    pvav_pfp = 'PVAV_PFP'
    pvav_ger = 'PVAV_BoilerElectricReheat'


class PSZEquipmentType(str, Enum):
    psz_e_base = 'PSZAC_ElectricBaseboard'
    psz_gb_base = 'PSZAC_BoilerBaseboard'
    psz_dhw_base = 'PSZAC_DHWBaseboard'
    psz_guh = 'PSZAC_GasHeaters'
    psz_ec = 'PSZAC_ElectricCoil'
    psz_gc = 'PSZAC_GasCoil'
    psz_gb = 'PSZAC_Boiler'
    psz_ashp = 'PSZAC_ASHP'
    psz_dhw = 'PSZAC_DHW'
    psz_ac = 'PSZAC'
    psz_dcw_e_base = 'PSZAC_DCW_ElectricBaseboard'
    psz_dcw_gb_base = 'PSZAC_DCW_BoilerBaseboard'
    psz_dcw_guh = 'PSZAC_DCW_GasHeaters'
    psz_dcw_ec = 'PSZAC_DCW_ElectricCoil'
    psz_dcw_gc = 'PSZAC_DCW_GasCoil'
    psz_dcw_gb = 'PSZAC_DCW_Boiler'
    psz_dcw_ashp = 'PSZAC_DCW_ASHP'
    psz_dcw_dhw = 'PSZAC_DCW_DHW'
    psz_dcw_ac = 'PSZAC_DCW'
    psz_hp = 'PSZHP'


class PTACEquipmentType(str, Enum):
    ptac_e_base = 'PTAC_ElectricBaseboard'
    ptac_gb_base = 'PTAC_BoilerBaseboard'
    ptac_dhw_base = 'PTAC_DHWBaseboard'
    ptac_guh = 'PTAC_GasHeaters'
    ptac_ec = 'PTAC_ElectricCoil'
    ptac_gc = 'PTAC_GasCoil'
    ptac_gb = 'PTAC_Boiler'
    ptac_ashp = 'PTAC_ASHP'
    ptac_dhw = 'PTAC_DHW'
    ptac = 'PTAC'
    pthp = 'PTHP'


class FurnaceEquipmentType(str, Enum):
    furnace = 'Furnace'


class VAV(_AllAirBase):
    """Variable Air Volume (VAV) HVAC system."""

    type: constr(regex='^VAV$') = 'VAV'

    equipment_type: VAVEquipmentType = Field(
        VAVEquipmentType.vav_chill_gbr,
        description='Text for the specific type of system equipment from the '
        'VAVEquipmentType enumeration.'
    )


class PVAV(_AllAirBase):
    """Packaged Variable Air Volume (PVAV) HVAC system."""

    type: constr(regex='^PVAV$') = 'PVAV'

    equipment_type: PVAVEquipmentType = Field(
        PVAVEquipmentType.pvav_gbr,
        description='Text for the specific type of system equipment from the '
        'VAVEquipmentType enumeration.'
    )


class PSZ(_AllAirBase):
    """Packaged Single-Zone (PSZ) HVAC system."""

    type: constr(regex='^PSZ$') = 'PSZ'

    equipment_type: PSZEquipmentType = Field(
        PSZEquipmentType.psz_e_base,
        description='Text for the specific type of system equipment from the '
        'PVAVEquipmentType enumeration.'
    )


class PTAC(_AllAirBase):
    """Packaged Terminal Air Conditioning (PTAC) or Heat Pump (PTHP) HVAC system."""

    type: constr(regex='^PTAC$') = 'PTAC'

    equipment_type: PTACEquipmentType = Field(
        PTACEquipmentType.ptac_e_base,
        description='Text for the specific type of system equipment from the '
        'PTACEquipmentType enumeration.'
    )


class ForcedAirFurnace(_AllAirBase):
    """Forced Air Furnace HVAC system. Intended for spaces only requiring heating."""

    type: constr(regex='^ForcedAirFurnace$') = 'ForcedAirFurnace'

    equipment_type: FurnaceEquipmentType = Field(
        FurnaceEquipmentType.furnace,
        description='Text for the specific type of system equipment from the '
        'FurnaceEquipmentType enumeration.'
    )
