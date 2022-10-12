"""Heating/cooling systems without any ventilation."""
from pydantic import Field, constr
from enum import Enum

from ._template import _TemplateSystem, RadiantFaceTypes


class _HeatCoolBase(_TemplateSystem):
    """Base class for all heating/cooling systems without any ventilation.

    These systems are only designed to satisfy heating + cooling demand and they
    cannot meet any minimum ventilation requirements.

    As such, these systems tend to be used in residential or storage settings where
    meeting minimum ventilation requirements may not be required or the density
    of occupancy is so low that infiltration is enough to meet fresh air demand.
    """


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


class RadiantEquipmentType(str, Enum):
    radiant_chill_gb = 'Radiant_Chiller_Boiler'
    radiant_chill_ashp = 'Radiant_Chiller_ASHP'
    radiant_chill_dhw = 'Radiant_Chiller_DHW'
    radiant_ac_chill_gb = 'Radiant_ACChiller_Boiler'
    radiant_ac_chill_ashp = 'Radiant_ACChiller_ASHP'
    radiant_ac_chill_dhw = 'Radiant_ACChiller_DHW'
    radiant_dcw_gb = 'Radiant_DCW_Boiler'
    radiant_dcw_ashp = 'Radiant_DCW_ASHP'
    radiant_dcw_dhw = 'Radiant_DCW_DHW'


class FCU(_HeatCoolBase):
    """Fan Coil Unit (FCU) heating/cooling system (with no ventilation).

    Each room/zone receives its own Fan Coil Unit (FCU), which meets the heating
    and cooling loads of the space. The cooling coil in the FCU is always chilled
    water cooling coil, which is connected to a chilled water loop operating
    at 6.7C (44F). The heating coil is a hot water coil except when when electric
    baseboards or gas heaters are specified. Hot water temperature is 82C (180F) for
    boiler/district heating and 49C (120F) when ASHP is used.
    """

    type: constr(regex='^FCU$') = 'FCU'

    equipment_type: FCUEquipmentType = Field(
        FCUEquipmentType.fcu_chill_gb,
        description='Text for the specific type of system equipment from the '
        'FCUEquipmentType enumeration.'
    )


class Baseboard(_HeatCoolBase):
    """Baseboard heating system.

    Baseboard systems are intended for spaces only requiring heating and
    no ventilation or cooling. Each room/zone will get its own baseboard
    heating unit that satisfies the heating load.
    """

    type: constr(regex='^Baseboard$') = 'Baseboard'

    equipment_type: BaseboardEquipmentType = Field(
        BaseboardEquipmentType.e_base,
        description='Text for the specific type of system equipment from the '
        'BaseboardEquipmentType enumeration.'
    )


class EvaporativeCooler(_HeatCoolBase):
    """Direct evaporative cooling systems (with optional heating).

    Each room/zone will receive its own air loop sized to meet the sensible load,
    which contains an evaporative cooler that directly adds humidity to the room
    air to cool it. The loop contains an outdoor air mixer, which is used whenever
    the outdoor air has a lower wet bulb temperature than the return air from
    the room. In the event that the combination of outdoor and room return air
    air is too humid, a backup single-speed direct expansion (DX) cooling coil
    will be used. Heating loads can be met with various options, including
    several types of baseboards, a furnace, or gas unit heaters.
    """

    type: constr(regex='^EvaporativeCooler$') = 'EvaporativeCooler'

    equipment_type: EvaporativeCoolerEquipmentType = Field(
        EvaporativeCoolerEquipmentType.evap_e_base,
        description='Text for the specific type of system equipment from the '
        'EvaporativeCoolerEquipmentType enumeration.'
    )


class WSHP(_HeatCoolBase):
    """Water Source Heat Pump (WSHP) heating/cooling system (with no ventilation).

    Each room/zone receives its own Water Source Heat Pump (WSHP), which meets
    the heating and cooling loads of the space. All WSHPs are connected to the
    same water condenser loop, which has its temperature maintained by the
    equipment_type (eg. Boiler with Cooling Tower).
    """

    type: constr(regex='^WSHP$') = 'WSHP'

    equipment_type: WSHPEquipmentType = Field(
        WSHPEquipmentType.wshp_fc_gb,
        description='Text for the specific type of system equipment from the '
        'WSHPEquipmentType enumeration.'
    )


class Residential(_HeatCoolBase):
    """Residential Air Conditioning, Heat Pump or Furnace system.

    Residential HVAC systems are intended primarily for single-family homes and
    include a wide variety of options. In all cases, each room/zone will receive
    its own air loop WITHOUT an outdoor air inlet (air is simply being recirculated
    through the loop). Residential air conditioning (AC) systems are modeled
    using a unitary system with a single-speed direct expansion (DX) cooling
    coil in the loop. Residential heat pump (HP) systems use a single-speed DX
    heating coil in the unitary system and the residential furnace option uses
    a gas coil in the unitary system. In all cases, the properties of these coils
    are set to reflect a typical residential system.
    """

    type: constr(regex='^Residential$') = 'Residential'

    equipment_type: ResidentialEquipmentType = Field(
        ResidentialEquipmentType.res_ac_e_base,
        description='Text for the specific type of system equipment from the '
        'ResidentialEquipmentType enumeration.'
    )


class WindowAC(_HeatCoolBase):
    """Window Air Conditioning cooling system (with optional heating).

    Each room/zone will receive its own Packaged Terminal Air Conditioner (PTAC)
    with properties set to reflect a typical window air conditioning (AC) unit.
    No ventilation air is supplied by the unit and the cooling coil within the
    unit is a single-speed direct expansion (DX) cooling coil. Heating loads
    can be met with various options, including several types of baseboards,
    a furnace, or gas unit heaters.
    """

    type: constr(regex='^WindowAC$') = 'WindowAC'

    equipment_type: WindowACEquipmentType = Field(
        WindowACEquipmentType.win_ac_e_base,
        description='Text for the specific type of system equipment from the '
        'WindowACEquipmentType enumeration.'
    )


class VRF(_HeatCoolBase):
    """Variable Refrigerant Flow (VRF) heating/cooling system (with no ventilation).

    Each room/zone receives its own Variable Refrigerant Flow (VRF) terminal,
    which meets the heating and cooling loads of the space. All room/zone terminals
    are connected to the same outdoor unit, meaning that either all rooms must be
    in cooling or heating mode together.
    """

    type: constr(regex='^VRF$') = 'VRF'

    equipment_type: VRFEquipmentType = Field(
        VRFEquipmentType.vrf,
        description='Text for the specific type of system equipment from the '
        'VRFEquipmentType enumeration.'
    )


class GasUnitHeater(_HeatCoolBase):
    """Gas unit heating system.

    Gas unit systems are intended for spaces only requiring heating and no
    ventilation or cooling. Each room/zone will get its own gaa heating unit
    that satisfies the heating load.
    """

    type: constr(regex='^GasUnitHeater$') = 'GasUnitHeater'

    equipment_type: GasUnitHeaterEquipmentType = Field(
        GasUnitHeaterEquipmentType.guh,
        description='Text for the specific type of system equipment from the '
        'GasUnitHeaterEquipmentType enumeration.'
    )


class Radiant(_HeatCoolBase):
    """Low temperature radiant HVAC system.

    This HVAC template will change the floor and/or ceiling constructions
    of the Rooms that it is applied to, replacing them with a construction that
    aligns with the radiant_type property (eg. CeilingMetalPanel).

    The heating and cooling needs of the space are met with the radiant constructions,
    which use chilled water at 12.8C (55F) and a hot water temperature somewhere
    between 32.2C (90F) and 49C (120F) (warmer temperatures are used in colder
    climate zones).

    Note that radiant systems are particularly limited in cooling capacity and
    using them may result in many unmet hours. To reduce unmet hours, one can
    remove carpets, reduce internal loads, reduce solar and envelope gains during
    peak times, add thermal mass, and use an expanded comfort range.
    """

    type: constr(regex='^Radiant$') = 'Radiant'

    equipment_type: RadiantEquipmentType = Field(
        RadiantEquipmentType.radiant_chill_gb,
        description='Text for the specific type of system equipment from the '
        'RadiantEquipmentType enumeration.'
    )

    radiant_face_type: RadiantFaceTypes = Field(
        RadiantFaceTypes.floor,
        description='Text to indicate which faces are thermally active by default. '
        'Note that this property has no effect when the rooms to which the HVAC '
        'system is assigned have constructions with internal source materials. '
        'In this case, those constructions will dictate the thermally active '
        'surfaces.'
    )

    minimum_operation_time: float = Field(
        1.0,
        gt=0,
        description='A number for the minimum number of hours of operation '
        'for the radiant system before it shuts off.'
    )

    switch_over_time: float = Field(
        24.0,
        gt=0,
        description='A number for the minimum number of hours for when the system '
        'can switch between heating and cooling.'
    )
