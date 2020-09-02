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
    vav_chill_gbr = 'VAV chiller with gas boiler reheat'
    vav_chill_ashp = 'VAV chiller with central air source heat pump reheat'
    vav_chill_dhw = 'VAV chiller with district hot water reheat'
    vav_chill_pfp = 'VAV chiller with PFP boxes'
    vav_chill_gcr = 'VAV chiller with gas coil reheat'
    vav_ac_chill_gbr = 'VAV air-cooled chiller with gas boiler reheat'
    vav_ac_chill_ashp = 'VAV air-cooled chiller with central air source heat pump reheat'
    vav_ac_chill_dhw = 'VAV air-cooled chiller with district hot water reheat'
    vav_ac_chill_pfp = 'VAV air-cooled chiller with PFP boxes'
    vav_ac_chill_gcr = 'VAV air-cooled chiller with gas coil reheat'
    vav_dcw_gbr = 'VAV district chilled water with gas boiler reheat'
    vav_dcw_ashp = 'VAV district chilled water with central air source heat pump reheat'
    vav_dcw_dhw = 'VAV district chilled water with district hot water reheat'
    vav_dcw_pfp = 'VAV district chilled water with PFP boxes'
    vav_dcw_gcr = 'VAV district chilled water with gas coil reheat'


class PVAVEquipmentType(str, Enum):
    pvav_gbr = 'PVAV with gas boiler reheat'
    pvav_ashp = 'PVAV with central air source heat pump reheat'
    pvav_dhw = 'PVAV with district hot water reheat'
    pvav_pfp = 'PVAV with PFP boxes'
    pvav_ger = 'PVAV with gas heat with electric reheat'


class PSZEquipmentType(str, Enum):
    psz_e_base = 'PSZ-AC with baseboard electric'
    psz_gb_base = 'PSZ-AC with baseboard gas boiler'
    psz_dhw_base = 'PSZ-AC with baseboard district hot water'
    psz_guh = 'PSZ-AC with gas unit heaters'
    psz_ec = 'PSZ-AC with electric coil'
    psz_gc = 'PSZ-AC with gas coil'
    psz_gb = 'PSZ-AC with gas boiler'
    psz_ashp = 'PSZ-AC with central air source heat pump'
    psz_dhw = 'PSZ-AC with district hot water'
    psz_ac = 'PSZ-AC with no heat'
    psz_dcw_e_base = 'PSZ-AC district chilled water with baseboard electric'
    psz_dcw_gb_base = 'PSZ-AC district chilled water with baseboard gas boiler'
    psz_dcw_dhw_base = 'PSZ-AC district chilled water with baseboard district hot water'
    psz_dcw_guh = 'PSZ-AC district chilled water with gas unit heaters'
    psz_dcw_ec = 'PSZ-AC district chilled water with electric coil'
    psz_dcw_gc = 'PSZ-AC district chilled water with gas coil'
    psz_dcw_gb = 'PSZ-AC district chilled water with gas boiler'
    psz_dcw_ashp = 'PSZ-AC district chilled water with central air source heat pump'
    psz_dcw_dhw = 'PSZ-AC district chilled water with district hot water'
    psz_dcw_ac = 'PSZ-AC district chilled water with no heat'
    psz_hp = 'PSZ-HP'


class PTACEquipmentType(str, Enum):
    ptac_e_base = 'PTAC with baseboard electric'
    ptac_gb_base = 'PTAC with baseboard gas boiler'
    ptac_dhw_base = 'PTAC with baseboard district hot water'
    ptac_guh = 'PTAC with gas unit heaters'
    ptac_ec = 'PTAC with electric coil'
    ptac_gc = 'PTAC with gas coil'
    ptac_gb = 'PTAC with gas boiler'
    ptac_ashp = 'PTAC with central air source heat pump'
    ptac_dhw = 'PTAC with district hot water'
    ptac = 'PTAC with no heat'
    pthp = 'PTHP'


class FurnaceEquipmentType(str, Enum):
    furnace = 'Forced air furnace'


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
