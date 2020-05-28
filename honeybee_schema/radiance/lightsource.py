"""SensorGrid and Sensor Schema"""
from pydantic import Field, constr
from typing import Optional

from .._base import NoExtraBaseModel
from .wea import Wea


class _GlowHemisphere(NoExtraBaseModel):
    """Hidden base class for Ground and SkyHemisphere."""

    r_emittance: float = Field(
        default=1.0,
        ge=0,
        le=1,
        description='A value between 0 and 1 for the red channel emittance.'
    )

    g_emittance: float = Field(
        default=1.0,
        ge=0,
        le=1,
        description='A value between 0 and 1 for the green channel emittance.'
    )

    b_emittance: float = Field(
        default=1.0,
        ge=0,
        le=1,
        description='A value between 0 and 1 for the blue channel of the emittance.'
    )


class Ground(_GlowHemisphere):
    """Ground component of the sky sphere."""

    type: constr(regex='^Ground$') = 'Ground'


class SkyHemisphere(_GlowHemisphere):
    """SkyHemisphere component of the sky sphere."""

    type: constr(regex='^SkyHemisphere$') = 'SkyHemisphere'


class SkyDome(NoExtraBaseModel):
    """Base class for all sky domes."""

    type: constr(regex='^SkyDome$') = 'SkyDome'

    ground_hemisphere: Optional[Ground] = Field(
        default=Ground(),
        description='Optional ground glow source.'
    )

    sky_hemisphere: Optional[SkyHemisphere] = Field(
        default=SkyHemisphere(),
        description='Optional sky hemisphere glow source.'
    )


class _PointInTime(SkyDome):
    """Hidden base class for all point-in-time sky domes."""

    ground_reflectance: float = Field(
        default=0.2,
        ge=0,
        le=1,
        description='A value between 0 and 1 for the ground reflectance.'
    )


class _SkyWithSun(_PointInTime):
    """Hidden base class for all altitude/azimuth sky domes."""

    altitude: float = Field(
        ...,
        ge=-90,
        le=90,
        description='The solar altitude measured in degrees above the horizon.'
        'Negative values indicate cases where the sun is below the horizon '
        '(eg. twilight conditions).'
    )

    azimuth: float = Field(
        ...,
        ge=0,
        le=360,
        description='The solar altitude measured in degrees above the horizon.'
        'The azimuth is measured in degrees east of North. East is 90, South is 180 and '
        'West is 270. Note that this input is different from Radiance convention. In '
        'Radiance the azimuth degrees are measured in west of South.'
    )


class CertainIrradiance(_PointInTime):
    """Sky with evenly distributed light at a certain irradiance value."""

    type: constr(regex='^CertainIrradiance$') = 'CertainIrradiance'

    irradiance: float = Field(
        default=558.659,
        ge=0,
        description='A value for the horizontal diffuse irradiance value in W/m2.'
    )


class CIE(_SkyWithSun):
    """CIE sky similar to using Radiance's gensky command."""

    type: constr(regex='^CIE$') = 'CIE'

    sky_type: int = Field(
        0,
        ge=0,
        le=5,
        description='An integer between 0..5 to indicate CIE Sky Type.'
        '\n0 = Sunny with sun.'
        '\n1 = Sunny without sun.'
        '\n2 = Intermediate with sun.'
        '\n3 = Intermediate without sun.'
        '\n4 = Cloudy sky.'
        '\n5 = Uniform cloudy sky.'
    )


class ClimateBased(_SkyWithSun):
    """Point-in-time Climate-based sky."""

    type: constr(regex='^ClimateBased$') = 'ClimateBased'

    direct_normal_irradiance: float = Field(
        ...,
        ge=0,
        description='Direct normal irradiance (W/m2).'
    )

    diffuse_horizontal_irradiance: float = Field(
        ...,
        ge=0,
        description='Diffuse horizontal irradiance (W/m2).'
    )


class SunMatrix(NoExtraBaseModel):
    """Annual Climate-based Sun matrix."""

    type: constr(regex='^SunMatrix$') = 'SunMatrix'

    wea: Wea = Field(
        ...,
        description='A Ladybug wea schema.'
    )

    north: float = Field(
        0,
        ge=-360,
        le=360,
        description='A number between -360 and 360 for the counterclockwise '
        'difference between the North and the positive Y-axis in degrees. '
        '90 is West and 270 is East.'
    )


class SkyMatrix(SunMatrix):
    """Annual Climate-based Sky matrix."""

    type: constr(regex='^SkyMatrix$') = 'SkyMatrix'

    density: int = Field(
        1,
        ge=1,
        description='Sky patch subdivision density. This values is similar to '
        '-m option in gendaymtx command. Default is 1 which means 145 sky patches '
        'and 1 patch for the ground. One can add to the resolution typically by '
        'factors of two (2, 4, 8, ...) which yields a higher resolution sky using '
        'the Reinhart patch subdivision.'
    )
