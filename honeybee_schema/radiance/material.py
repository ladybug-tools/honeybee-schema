"""Material Schema"""
from pydantic import Field, constr
from typing import List, Union

from .primitive import Primitive


# TODO: Do we to create and inherit Material/Modifier class?
# There are no setable properties in both.
class Plastic(Primitive):
    """Radiance plastic material."""

    type: constr(regex='^Plastic$') = 'Plastic'

    r_reflectance: float = Field(
        default=0.0,
        ge=0,
        le=1,
        description='A value between 0 and 1 for the red channel reflectance '
                    '(Default: 0).'
    )

    g_reflectance: float = Field(
        default=0.0,
        ge=0,
        le=1,
        description='A value between 0 and 1 for the green channel reflectance '
                    '(Default: 0).'
    )

    b_reflectance: float = Field(
        default=0.0,
        ge=0,
        le=1,
        description='A value between 0 and 1 for the blue channel reflectance '
                    '(Default: 0).'
    )

    specularity: float = Field(
        default=0,
        ge=0,
        le=1,
        description='A value between 0 and 1 for the fraction of specularity. '
                    'Specularity fractions greater than 0.1 are not realistic. '
                    '(Default: 0).'
    )

    roughness: float = Field(
        default=0,
        ge=0,
        le=1,
        description='A value between 0 and 1 for the roughness, specified as the '
                    'rms slope of surface facets. Roughness greater than 0.2 are '
                    'not realistic (Default: 0).'
    )


# TODO: Check if this is correct? Everything here is inherited
# from Plastic w/e of 'type'.
class Metal(Plastic):
    """Radiance metal material."""

    type: constr(regex='^Metal$') = 'Metal'


# TODO: Do we to create and inherit Material/Modifier class?
# There are no setable properties in both.
class Glass(Primitive):
    """Radiance glass material."""

    type: constr(regex='^Glass$') = 'Glass'

    r_transmissivity: float = Field(
        default=0.0,
        ge=0,
        le=1,
        description='A value between 0 and 1 for the red channel transmissivity '
                    '(Default: 0).'
    )

    g_transmissivity: float = Field(
        default=0.0,
        ge=0,
        le=1,
        description='A value between 0 and 1 for the green channel transmissivity '
                    '(Default: 0).'
    )

    b_transmissivity: float = Field(
        default=0.0,
        ge=0,
        le=1,
        description='A value between 0 and 1 for the blue channel transmissivity '
                    '(Default: 0).'
    )

    refraction_index: float = Field(
        default=1.52,
        ge=0,
        le=1,
        description='A value between 0 and 1 for the index of refraction '
                    '(Default: 1.52).'
    )


if __name__ == '__main__':
    print(Plastic.schema_json(indent=2))
    print(Metal.schema_json(indent=2))
    print(Glass.schema_json(indent=2))