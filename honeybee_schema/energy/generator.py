"""Schemas for objects that generate electricity."""
from pydantic import Field, constr

from .._base import NoExtraBaseModel
from ._base import EnergyBaseModel
from enum import Enum


class ElectricLoadCenter(NoExtraBaseModel):

    type: constr(regex='^ElectricLoadCenter$') = 'ElectricLoadCenter'

    inverter_efficiency: float = Field(
        0.96,
        gt=0,
        le=1,
        description='A number between 0 and 1 for the load center inverter nominal '
        'rated DC-to-AC conversion efficiency. An inverter converts DC power, such '
        'as that output by photovoltaic panels, to AC power, such as that distributed '
        'by the electrical grid and is available from standard electrical outlets. '
        'Inverter efficiency is defined as the inverter rated AC power output divided '
        'by its rated DC power output.'
    )

    inverter_dc_to_ac_size_ratio: float = Field(
        1.1,
        gt=0,
        description='A positive number (typically greater than 1) for the ratio of '
        'the inverter DC rated size to its AC rated size. Typically, inverters are '
        'not sized to convert the full DC output under standard test conditions (STC) '
        'as such conditions rarely occur in reality and therefore unnecessarily add '
        'to the size/cost of the inverter. For a system with a high DC to AC size '
        'ratio, during times when the DC power output exceeds the inverter rated '
        'DC input size, the inverter limits the power output by increasing the '
        'DC operating voltage, which moves the arrays operating point down its '
        'current-voltage (I-V) curve. In EnergyPlus, this is accomplished by simply '
        'limiting the system output to the AC size as dictated by the ratio. The '
        'default value of 1.1 is reasonable for most systems. A typical range is '
        '1.1 to 1.25, although some large-scale systems have ratios of as high '
        'as 1.5. The optimal value depends on the system location, array '
        'orientation, and module cost.'
    )


class ModuleType(str, Enum):
    standard = 'Standard'
    premium = 'Premium'
    thin_film = 'ThinFilm'


class MountingType(str, Enum):
    fixed_open_rack = 'FixedOpenRack'
    fixed_roof_mounted = 'FixedRoofMounted'
    one_axis = 'OneAxis'
    one_axis_backtracking = 'OneAxisBacktracking'
    two_axis = 'TwoAxis'


class PVProperties(EnergyBaseModel):

    type: constr(regex='^PVProperties$') = 'PVProperties'

    rated_efficiency: float = Field(
        0.15,
        gt=0,
        lt=1,
        description='A number between 0 and 1 for the rated nameplate efficiency '
        'of the photovoltaic solar cells under standard test conditions (STC). '
        'Standard test conditions are 1,000 Watts per square meter solar '
        'irradiance, 25 degrees C cell temperature, and ASTM G173-03 standard '
        'spectrum. Nameplate efficiencies reported by manufacturers are typically '
        'under STC. Standard poly- or mono-crystalline silicon modules tend to have '
        'rated efficiencies in the range of 14-17%. Premium high efficiency '
        'mono-crystalline silicon modules with anti-reflective coatings can have '
        'efficiencies in the range of 18-20%. Thin film photovoltaic modules '
        'typically have efficiencies of 11% or less. (Default: 0.15 for standard '
        'silicon solar cells).'
    )

    active_area_fraction: float = Field(
        0.9,
        gt=0,
        le=1,
        description='The fraction of the parent Shade geometry that is '
        'covered in active solar cells. This fraction includes the difference '
        'between the PV panel (aka. PV module) area and the active cells within '
        'the panel as well as any losses for how the (typically rectangular) panels '
        'can be arranged on the Shade geometry. When the parent Shade geometry '
        'represents just the solar panels, this fraction is typically around 0.9 '
        'given that the framing elements of the panel reduce the overall '
        'active area. (Default: 0.9, assuming parent Shade geometry represents '
        'only the PV panel geometry).'
    )

    module_type: ModuleType = Field(
        default=ModuleType.standard,
        description='Text to indicate the type of solar module. This is used to '
        'determine the temperature coefficients used in the simulation of the '
        'photovoltaic modules. When the rated_efficiency is between 12-18%, the '
        'Standard type is typically most appropriate. When the rated_efficiency is '
        'greater than 18%, the Premium type is likely more appropriate. When '
        'the rated_efficiency is less than 12%, this likely refers to a case where '
        'the ThinFilm module type is most appropriate.'
    )

    mounting_type: MountingType = Field(
        default=MountingType.fixed_open_rack,
        description='Text to indicate the type of mounting and/or tracking used '
        'for the photovoltaic array. Note that the OneAxis options have an axis '
        'of rotation that is determined by the azimuth of the parent Shade '
        'geometry. Also note that, in the case of one or two axis tracking, '
        'shadows on the (static) parent Shade geometry still reduce the '
        'electrical output, enabling the simulation to account for large '
        'context geometry casting shadows on the array. However, the effects '
        'of smaller detailed shading may be improperly accounted for and self '
        'shading of the dynamic panel geometry is only accounted for via the '
        'tracking_ground_coverage_ratio property on this object. FixedOpenRack '
        'refers to ground or roof mounting where the air flows freely. FixedRoofMounted '
        'refers to mounting flush with the roof with limited air flow. OneAxis '
        'refers to a fixed tilt and azimuth, which define an axis of rotation. '
        'OneAxisBacktracking is the same as OneAxis but with controls to reduce '
        'self-shade at low sun angles. TwoAxis refers to a dynamic tilt and '
        'azimuth that track the sun.'
    )

    system_loss_fraction: float = Field(
        0.14,
        ge=0,
        le=1,
        description='A number between 0 and 1 for the fraction of the electricity '
        'output lost due to factors other than EPW weather conditions, '
        'panel efficiency/type, active area, mounting, and inverter conversion from '
        'DC to AC. Factors that should be accounted for in this input include '
        'soiling, snow, wiring losses, electrical connection losses, manufacturer '
        'defects/tolerances/mismatch in cell characteristics, losses from power '
        'grid availability, and losses due to age or light-induced degradation. '
        'Losses from these factors tend to be between 10-20% but can vary widely '
        'depending on the installation, maintenance and the grid to which the '
        'panels are connected..'
    )
