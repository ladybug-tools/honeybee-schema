"""All-air HVAC systems, providing ventilation and meeting thermal demand with air."""
from pydantic import Field, constr
from enum import Enum

from ._template import _TemplateSystem


class AllAirEconomizerType(str, Enum):
    no_economizer = 'NoEconomizer'
    differential_dry_bulb = 'DifferentialDryBulb'
    differential_enthalpy = 'DifferentialEnthalpy'
    differential_dry_bulb_and_enthalpy = 'DifferentialDryBulbAndEnthalpy'
    fixed_dry_bulb = 'FixedDryBulb'
    fixed_enthalpy = 'FixedEnthalpy'
    electronic_enthalpy = 'ElectronicEnthalpy'


class _AllAirBase(_TemplateSystem):
    """Base class for all-air systems.

    All-air systems provide both ventilation and heating + cooling demand with
    the same stream of warm/cool air. As such, they often grant tight control
    over zone humidity. However, because such systems often involve the
    cooling of air only to reheat it again, they are often more energy intensive
    than systems that separate ventilation from the meeting of thermal loads.
    """

    economizer_type: AllAirEconomizerType = Field(
        AllAirEconomizerType.no_economizer,
        description='Text to indicate the type of air-side economizer used on '
        'the system (from the AllAirEconomizerType enumeration).'
    )

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
    furnace_electric = 'Furnace_Electric'


class VAV(_AllAirBase):
    """Variable Air Volume (VAV) HVAC system (aka. System 7 or 8).

    All rooms/zones are connected to a central air loop that is kept at a constant
    central temperature of 12.8C (55F). The central temperature is maintained by a
    cooling coil, which runs whenever the combination of return air and fresh outdoor
    air is greater than 12.8C, as well as a heating coil, which runs whenever
    the combination of return air and fresh outdoor air is less than 12.8C.

    Each air terminal for the connected rooms/zones contains its own reheat coil,
    which runs whenever the room is not in need of the cooling supplied by the 12.8C
    central air.

    The central cooling coil is always a chilled water coil, which is connected to a
    chilled water loop operating at 6.7C (44F). All heating coils are hot water coils
    except when Gas Coil equipment_type is used (in which case coils are gas)
    or when Parallel Fan-Powered (PFP) boxes equipment_type is used (in which case
    coils are electric resistance). Hot water temperature is 82C (180F) for
    boiler/district heating and 49C (120F) when ASHP is used.

    VAV systems are the traditional baseline system for commercial buildings
    taller than 5 stories or larger than 14,000 m2 (150,000 ft2) of floor area.
    """

    type: constr(regex='^VAV$') = 'VAV'

    equipment_type: VAVEquipmentType = Field(
        VAVEquipmentType.vav_chill_gbr,
        description='Text for the specific type of system equipment from the '
        'VAVEquipmentType enumeration.'
    )


class PVAV(_AllAirBase):
    """Packaged Variable Air Volume (PVAV) HVAC system (aka. System 5 or 6).

    All rooms/zones are connected to a central air loop that is kept at a constant
    central temperature of 12.8C (55F). The central temperature is maintained by a
    cooling coil, which runs whenever the combination of return air and fresh outdoor
    air is greater than 12.8C, as well as a heating coil, which runs whenever
    the combination of return air and fresh outdoor air is less than 12.8C.

    Each air terminal for the connected rooms/zones contains its own reheat coil,
    which runs whenever the room is not in need of the cooling supplied by the 12.8C
    central air.

    The central cooling coil is always a two-speed direct expansion (DX) coil.
    All heating coils are hot water coils except when Gas Coil equipment_type is
    used (in which case the central coil is gas and all reheat is electric)
    or when Parallel Fan-Powered (PFP) boxes equipment_type is used (in which case
    coils are electric resistance). Hot water temperature is 82C (180F) for
    boiler/district heating and 49C (120F) when ASHP is used.

    PVAV systems are the traditional baseline system for commercial buildings
    with than 4-5 stories or between 2,300 m2 and 14,000 m2 (25,000 ft2 and
    150,000 ft2) of floor area.
    """

    type: constr(regex='^PVAV$') = 'PVAV'

    equipment_type: PVAVEquipmentType = Field(
        PVAVEquipmentType.pvav_gbr,
        description='Text for the specific type of system equipment from the '
        'VAVEquipmentType enumeration.'
    )


class PSZ(_AllAirBase):
    """Packaged Single-Zone (PSZ) HVAC system (aka. System 3 or 4).

    Each room/zone receives its own air loop with its own single-speed direct expansion
    (DX) cooling coil, which will condition the supply air to a value in between
    12.8C (55F) and 50C (122F) depending on the heating/cooling needs of the room/zone.
    As long as a Baseboard equipment_type is NOT selected, heating will be supplied
    by a heating coil in the air loop. Otherwise, heating is accomplished with
    baseboards and the air loop only supplies cooling and ventilation air.
    Fans are constant volume.

    PSZ systems are the traditional baseline system for commercial buildings
    with less than 4 stories or less than 2,300 m2 (25,000 ft2) of floor area.
    They are also the default for all retail with less than 3 stories and all public
    assembly spaces.
    """

    type: constr(regex='^PSZ$') = 'PSZ'

    equipment_type: PSZEquipmentType = Field(
        PSZEquipmentType.psz_e_base,
        description='Text for the specific type of system equipment from the '
        'PVAVEquipmentType enumeration.'
    )


class PTAC(_TemplateSystem):
    """Packaged Terminal Air Conditioning (PTAC/HP) HVAC system. (aka. System 1 or 2).

    Each room/zone receives its own packaged unit that supplies heating, cooling
    and ventilation. Cooling is always done via a single-speed direct expansion (DX)
    cooling coil. Heating can be done via a heating coil in the unit or via an
    external baseboard. Fans are constant volume.

    PTAC/HP systems are the traditional baseline system for residential buildings.
    """

    type: constr(regex='^PTAC$') = 'PTAC'

    equipment_type: PTACEquipmentType = Field(
        PTACEquipmentType.ptac_e_base,
        description='Text for the specific type of system equipment from the '
        'PTACEquipmentType enumeration.'
    )


class ForcedAirFurnace(_TemplateSystem):
    """Forced Air Furnace HVAC system (aka. System 9 or 10).

    Forced air furnaces are intended only for spaces only requiring heating and
    ventilation. Each room/zone receives its own air loop with its own gas heating
    coil, which will supply air at a temperature up to 50C (122F) to meet the
    heating needs of the room/zone. Fans are constant volume.

    ForcedAirFurnace systems are the traditional baseline system for storage
    spaces that only require heating.
    """

    type: constr(regex='^ForcedAirFurnace$') = 'ForcedAirFurnace'

    equipment_type: FurnaceEquipmentType = Field(
        FurnaceEquipmentType.furnace,
        description='Text for the specific type of system equipment from the '
        'FurnaceEquipmentType enumeration.'
    )
