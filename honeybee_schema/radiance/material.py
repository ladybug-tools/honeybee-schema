"""Material Schema"""
from pydantic import Field, constr
from typing import List, Union

from .._base import IDdBaseModel


class Void(IDdBaseModel):
    """Void modifier"""

    type: constr(regex='^Void$') = 'Void'


class ModifierBase(IDdBaseModel):
    """Base class for Radiance Modifiers"""

    # TODO: We can't define union of schema objects that haven't been
    # defined yet. We also can't move this down, because ModifierBase
    # is inherited by all these objects.
    modifier: Union[
         Void, Plastic, Glass, BSDF, Glow, Light, Trans
    ] = Field(
        # TODO: This needs to be fixed. How can we add add default=Void,
        # when Void is not serializable?
        default='void',
        description='Material modifier (default: Void).'
        )

    # TODO: We can't define union of schema objects that haven't been
    # defined yet. We also can't move this down, because ModifierBase
    # is inherited by all these objects.
    dependencies: List[
        Union[Void, Plastic, Glass, BSDF, Glow, Light, Trans]
    ] = Field(
        default=[],
        min_items=1,
        description='List of modifiers that this modifier depends on. '
                    'This argument is only useful for defining advanced modifiers '
                    'where the modifier is defined based on other modifiers '
                    '(default: []).'
        )


class Plastic(ModifierBase):
    """Radiance plastic material."""

    type: constr(regex='^Plastic$') = 'Plastic'

    r_reflectance: float = Field(
        default=0.0,
        ge=0,
        le=1,
        description='A value between 0 and 1 for the red channel reflectance '
                    '(default: 0).'
    )

    g_reflectance: float = Field(
        default=0.0,
        ge=0,
        le=1,
        description='A value between 0 and 1 for the green channel reflectance '
                    '(default: 0).'
    )

    b_reflectance: float = Field(
        default=0.0,
        ge=0,
        le=1,
        description='A value between 0 and 1 for the blue channel reflectance '
                    '(default: 0).'
    )

    specularity: float = Field(
        default=0,
        ge=0,
        le=1,
        description='A value between 0 and 1 for the fraction of specularity. '
                    'Specularity fractions greater than 0.1 are not realistic. '
                    '(default: 0).'
    )

    roughness: float = Field(
        default=0,
        ge=0,
        le=1,
        description='A value between 0 and 1 for the roughness, specified as the '
                    'rms slope of surface facets. Roughness greater than 0.2 are '
                    'not realistic (default: 0).'
    )


class Trans(Plastic):
    """Radiance Translucent material."""

    type: constr(regex='^Trans$') = 'Trans'

    transmitted_diff: float = Field(
        default=0,
        description='The fraction of transmitted light that is transmitted diffusely in '
                    'a scattering fashion (default: 0).'
    )

    transmitted_spec: float = Field(
        default=0,
        description='The fraction of transmitted light that is not diffusely scattered '
                    '(default: 0).'
    )


class Glass(ModifierBase):
    """Radiance glass material."""

    type: constr(regex='^Glass$') = 'Glass'

    r_transmissivity: float = Field(
        default=0.0,
        ge=0,
        le=1,
        description='A value between 0 and 1 for the red channel transmissivity '
                    '(default: 0).'
    )

    g_transmissivity: float = Field(
        default=0.0,
        ge=0,
        le=1,
        description='A value between 0 and 1 for the green channel transmissivity '
                    '(default: 0).'
    )

    b_transmissivity: float = Field(
        default=0.0,
        ge=0,
        le=1,
        description='A value between 0 and 1 for the blue channel transmissivity '
                    '(default: 0).'
    )

    refraction_index: float = Field(
        default=1.52,
        ge=0,
        le=1,
        description='A value between 0 and 1 for the index of refraction '
                    '(default: 1.52).'
    )


class BSDF(ModifierBase):
    """Radiance BSDF (Bidirectional Scattering Distribution Function) material."""

    type: constr(regex='^BSDF$') = 'BSDF'

    up_orientation: List[float] = Field(
        default=(0.01, 0.01, 1.00),
        description='Vector as sequence that sets the hemisphere that the BSDF material '
                    'faces. (default: (0.01, 0.01, 1.00).'
    )

    thickness: float = Field(
        default=0,
        description='Optional number to set the thickness of the BSDF material '
                    'Sign of thickness indicates whether proxied geometry is '
                    'behind the BSDF surface (when thickness is positive) or in '
                    'front (when thickness is negative)(default: 0).'
    )

    function_file: str = Field(
        default='.',
        min_length=1,
        max_length=100,
        description='Optional input for function file (default: ".").'
    )

    transform: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Optional transform input to scale the thickness and reorient '
                    'the up vector (default: None).'
    )

    bsdf_data: bytes = Field(
        ...,
        description='BSDF xml file data as bytes.'
    )

    front_diffuse_reflectance: List[float] = Field(
        default=None,
        description='Optional additional front diffuse reflectance as sequence of '
                    'numbers (default: None).'
    )

    back_diffuse_reflectance: List[float] = Field(
        default=None,
        description='Optional additional back diffuse reflectance as sequence of '
                    'numbers (default: None).'
    )

    diffuse_transmittance: List[float] = Field(
        default=None,
        description='Optional additional diffuse transmittance as sequence of '
                    'numbers (default: None).'
    )


class Glow(ModifierBase):
    """Radiance Glow material."""

    type: constr(regex='^Glow$') = 'Glow'

    r_emittance: float = Field(
        default=0.0,
        ge=0,
        le=1,
        description='A value between 0 and 1 for the red channel glow '
                    '(default: 0).'
    )

    g_emittance: float = Field(
        default=0.0,
        ge=0,
        le=1,
        description='A value between 0 and 1 for the green channel glow '
                    '(default: 0).'
    )

    b_emittance: float = Field(
        default=0.0,
        ge=0,
        le=1,
        description='A value between 0 and 1 for the blue channel glow '
                    '(default: 0).'
    )

    max_radius: float = Field(
        default=0,
        description='Maximum radius for shadow testing (default: 0). '
    )


class Light(ModifierBase):
    """Radiance Light material."""

    type: constr(regex='^Light$') = 'Light'

    r_emittance: float = Field(
        default=0.0,
        ge=0,
        le=1,
        description='A value between 0 and 1 for the red channel of the light '
                    '(default: 0).'
    )

    g_emittance: float = Field(
        default=0.0,
        ge=0,
        le=1,
        description='A value between 0 and 1 for the green channel of the light '
                    '(default: 0).'
    )

    b_emittance: float = Field(
        default=0.0,
        ge=0,
        le=1,
        description='A value between 0 and 1 for the blue channel of the light '
                    '(default: 0).'
    )


if __name__ == '__main__':
    print(ModifierBase.schema_json(indent=2))
    print(Void.schema_json(indent=2))
    print(Plastic.schema_json(indent=2))
    print(Glass.schema_json(indent=2))
    print(BSDF.schema_json(indent=2))
    print(Glow.schema_json(indent=2))
    print(Light.schema_json(indent=2))
    print(Trans.schema_json(indent=2))

