"""Construction Schema"""
from pydantic import Field, constr, root_validator
from typing import List, Union
from enum import Enum

from ._base import IDdEnergyBaseModel
from .material import EnergyMaterial, EnergyMaterialNoMass, \
    EnergyWindowMaterialGas, EnergyWindowMaterialGasCustom, \
    EnergyWindowMaterialGasMixture, EnergyWindowMaterialSimpleGlazSys, \
    EnergyWindowMaterialGlazing, EnergyWindowMaterialShade, EnergyWindowMaterialBlind
from .schedule import ScheduleRuleset, ScheduleFixedInterval


class OpaqueConstructionAbridged(IDdEnergyBaseModel):
    """Construction for opaque objects (Face, Shade, Door)."""

    type: constr(regex='^OpaqueConstructionAbridged$') = 'OpaqueConstructionAbridged'

    layers: List[constr(min_length=1, max_length=100)] = Field(
        ...,
        description='List of strings for opaque material identifiers. The order '
        'of the materials is from exterior to interior.',
        min_items=1,
        max_items=10
    )


class OpaqueConstruction(OpaqueConstructionAbridged):
    """Construction for opaque objects (Face, Shade, Door)."""

    type: constr(regex='^OpaqueConstruction$') = 'OpaqueConstruction'

    materials: List[Union[EnergyMaterial, EnergyMaterialNoMass]] = Field(
        ...,
        description='List of opaque materials. The order of the materials is '
        'from outside to inside.',
        min_items=1,
        max_items=10
    )


class WindowConstructionAbridged(IDdEnergyBaseModel):
    """Construction for window objects (Aperture, Door)."""

    type: constr(regex='^WindowConstructionAbridged$') = 'WindowConstructionAbridged'

    layers: List[constr(min_length=1, max_length=100)] = Field(
        ...,
        description='List of strings for glazing or gas material identifiers. The '
        'order of the materials is from exterior to interior. If a SimpleGlazSys '
        'material is used, it must be the only material in the construction. '
        'For multi-layered constructions, adjacent glass layers must be separated '
        'by one and only one gas layer.',
        min_items=1,
        max_items=8
    )


class WindowConstruction(WindowConstructionAbridged):
    """Construction for window objects (Aperture, Door)."""

    type: constr(regex='^WindowConstruction$') = 'WindowConstruction'

    materials: List[
        Union[
            EnergyWindowMaterialSimpleGlazSys, EnergyWindowMaterialGlazing,
            EnergyWindowMaterialGas, EnergyWindowMaterialGasCustom,
            EnergyWindowMaterialGasMixture
        ]
    ] = Field(
        ...,
        description='List of glazing and gas materials. The order of the materials '
        'is from outside to inside. If a SimpleGlazSys material is used, it must '
        'be the only material in the construction. For multi-layered constructions, '
        'adjacent glass layers must be separated by one and only one gas layer.',
        min_items=1,
        max_items=8
    )


class ShadeLocation(str, Enum):
    """Choices for where a shade material is located in a window assembly."""
    interior = 'Interior'
    between = 'Between'
    exterior = 'Exterior'


class ControlType(str, Enum):
    """Choices for how the shading device is controlled."""
    always_on = 'AlwaysOn'
    on_if_high_solar_on_window = 'OnIfHighSolarOnWindow'
    on_if_high_horizontal_solar = 'OnIfHighHorizontalSolar'
    on_if_high_outdoor_air_temperature = 'OnIfHighOutdoorAirTemperature'
    on_if_high_zone_air_temperature = 'OnIfHighZoneAirTemperature'
    on_if_high_zone_cooling = 'OnIfHighZoneCooling'
    on_night_if_low_outdoor_temp_and_off_day = 'OnNightIfLowOutdoorTempAndOffDay'
    on_night_if_low_inside_temp_and_off_day = 'OnNightIfLowInsideTempAndOffDay'
    on_night_if_heating_and_off_day = 'OnNightIfHeatingAndOffDay'


class WindowConstructionShadeAbridged(IDdEnergyBaseModel):
    """Construction for window objects with an included shade layer."""

    type: constr(regex='^WindowConstructionShadeAbridged$') = \
        'WindowConstructionShadeAbridged'

    window_construction: WindowConstructionAbridged = Field(
        ...,
        description='A WindowConstructionAbridged object that serves as the '
        '"switched off" version of the construction (aka. the "bare construction"). '
        'The shade_material and shade_location will be used to modify this '
        'starting construction.'
    )

    shade_material: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description='Identifier of a An EnergyWindowMaterialShade or an '
        'EnergyWindowMaterialBlind that serves as the shading layer for this '
        'construction. This can also be an EnergyWindowMaterialGlazing, which '
        'will indicate that the WindowConstruction has a dynamically-controlled '
        'glass pane like an electrochromic window assembly.'
    )

    shade_location: ShadeLocation = Field(
        ShadeLocation.interior,
        description='Text to indicate where in the window assembly the shade_material '
        'is located.  Note that the WindowConstruction must have at least one gas '
        'gap to use the "Between" option. Also note that, for a WindowConstruction '
        'with more than one gas gap, the "Between" option defalts to using the '
        'inner gap as this is the only option that EnergyPlus supports.'
    )

    control_type: ControlType = Field(
        ControlType.always_on,
        description='Text to indicate how the shading device is controlled, which '
        'determines when the shading is “on” or “off.”'
    )

    setpoint: float = Field(
        None,
        description='A number that corresponds to the specified control_type. '
        'This can be a value in (W/m2), (C) or (W) depending upon the control type.'
        'Note that this value cannot be None for any control type except "AlwaysOn."'
    )

    schedule: str = Field(
        None,
        min_length=1,
        max_length=100,
        description='An optional schedule identifier to be applied on top of the '
        'control_type. If None, the control_type will govern all behavior of '
        'the construction.'
    )

    @root_validator
    def check_setpoint_exists(cls, values):
        "Ensure the setpoint exists if control_type isn't AlwaysOn."
        control_type = values.get('control_type')
        setpoint = values.get('setpoint')
        if control_type != 'AlwaysOn':
            assert setpoint is not None, 'Control setpoint cannot ' \
                'be None for control type "{}"'.format(control_type)
        return values


class WindowConstructionShade(WindowConstructionShadeAbridged):
    """Construction for window objects (Aperture, Door)."""

    type: constr(regex='^WindowConstructionShade$') = 'WindowConstructionShade'

    window_construction: WindowConstruction = Field(
        ...,
        description='A WindowConstruction object that serves as the "switched off" '
        'version of the construction (aka. the "bare construction"). '
        'The shade_material and shade_location will be used to modify this '
        'starting construction.'
    )

    shade_material: Union[
        EnergyWindowMaterialShade, EnergyWindowMaterialBlind,
        EnergyWindowMaterialGlazing
    ] = Field(
        ...,
        description='Identifier of a An EnergyWindowMaterialShade or an '
        'EnergyWindowMaterialBlind that serves as the shading layer for this '
        'construction. This can also be an EnergyWindowMaterialGlazing, which '
        'will indicate that the WindowConstruction has a dynamically-controlled '
        'glass pane like an electrochromic window assembly.'
    )

    schedule: Union[ScheduleRuleset, ScheduleFixedInterval] = Field(
        None,
        description='An optional ScheduleRuleset or ScheduleFixedInterval to be '
        'applied on top of the control_type. If None, the control_type will govern '
        'all behavior of the construction.'
    )


class ShadeConstruction(IDdEnergyBaseModel):
    """Construction for Shade objects."""

    type: constr(regex='^ShadeConstruction$') = 'ShadeConstruction'

    solar_reflectance: float = Field(
        0.2,
        ge=0,
        le=1,
        description='A number for the solar reflectance of the construction.'
    )

    visible_reflectance: float = Field(
        0.2,
        ge=0,
        le=1,
        description='A number for the visible reflectance of the construction.'
    )

    is_specular: bool = Field(
        default=False,
        description='Boolean to note whether the reflection off the shade is diffuse '
        '(False) or specular (True). Set to True if the construction is '
        'representing a glass facade or a mirror material.'
    )


class AirBoundaryConstructionAbridged(IDdEnergyBaseModel):
    """Construction for Air Boundary objects."""

    type: constr(regex='^AirBoundaryConstructionAbridged$') = \
        'AirBoundaryConstructionAbridged'

    air_mixing_per_area: float = Field(
        0.1,
        ge=0,
        description='A positive number for the amount of air mixing between Rooms '
        'across the air boundary surface [m3/s-m2]. Default: 0.1 corresponds '
        'to average indoor air speeds of 0.1 m/s (roughly 20 fpm), which is '
        'typical of what would be induced by a HVAC system.'
    )

    air_mixing_schedule: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description='Identifier of a fractional schedule for the air mixing schedule '
        'across the construction.'
    )


class AirBoundaryConstruction(AirBoundaryConstructionAbridged):
    """Construction for Air Boundary objects."""

    type: constr(regex='^AirBoundaryConstruction$') = 'AirBoundaryConstruction'

    air_mixing_schedule: Union[ScheduleRuleset, ScheduleFixedInterval] = Field(
        ...,
        description='A fractional schedule as a ScheduleRuleset or '
        'ScheduleFixedInterval for the air mixing schedule across '
        'the construction.'
    )
