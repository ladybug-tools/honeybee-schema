"""Modifier Schema"""
from __future__ import annotations
from pydantic import Field, BaseModel, constr, validator
from typing import List, Union, Optional
from ._base import IDdRadianceBaseModel


class Void(BaseModel):
    """Void modifier"""

    type: constr(regex='^Void$') = 'Void'


class ModifierBase(IDdRadianceBaseModel):
    """Base class for Radiance Modifiers"""

    type: constr(regex='^ModifierBase$') = 'ModifierBase'


class Mirror(ModifierBase):
    """Radiance mirror material."""

    type: constr(regex='^Mirror$') = 'Mirror'

    modifier: Optional[_REFERENCE_UNION_MODIFIERS] = Field(
        default=Void(),
        description='Material modifier.'
    )

    dependencies: List[_REFERENCE_UNION_MODIFIERS] = Field(
        default=None,
        description='List of modifiers that this modifier depends on. This argument '
        'is only useful for defining advanced modifiers where the modifier is defined '
        'based on other modifiers.'
    )

    r_reflectance: float = Field(
        default=1,
        ge=0,
        le=1,
        description='A value between 0 and 1 for the red channel reflectance.'
    )

    g_reflectance: float = Field(
        default=1,
        ge=0,
        le=1,
        description='A value between 0 and 1 for the green channel reflectance.'
    )

    b_reflectance: float = Field(
        default=1,
        ge=0,
        le=1,
        description='A value between 0 and 1 for the blue channel reflectance.'
    )

    alternate_material: _REFERENCE_UNION_MODIFIERS = Field(
        default=None,
        description='An optional material (like the illum type) that may be used to '
        'specify a different material to be used for shading non-source rays. '
        'If None, this will keep the alternat_material as mirror. If this alternate '
        'material is given as Void, then the mirror surface will be invisible. '
        'Using Void is only appropriate if the surface hides other (more '
        'detailed) geometry with the same overall reflectance.'
    )


class Plastic(ModifierBase):
    """Radiance plastic material."""

    type: constr(regex='^Plastic$') = 'Plastic'

    modifier: Optional[_REFERENCE_UNION_MODIFIERS] = Field(
        default=Void(),
        description='Material modifier.'
    )

    dependencies: List[_REFERENCE_UNION_MODIFIERS] = Field(
        default=None,
        description='List of modifiers that this modifier depends on. This argument '
        'is only useful for defining advanced modifiers where the modifier is defined '
        'based on other modifiers.'
    )

    r_reflectance: float = Field(
        default=0.0,
        ge=0,
        le=1,
        description='A value between 0 and 1 for the red channel reflectance.'
    )

    g_reflectance: float = Field(
        default=0.0,
        ge=0,
        le=1,
        description='A value between 0 and 1 for the green channel reflectance.'
    )

    b_reflectance: float = Field(
        default=0.0,
        ge=0,
        le=1,
        description='A value between 0 and 1 for the blue channel reflectance.'
    )

    specularity: float = Field(
        default=0,
        ge=0,
        le=1,
        description='A value between 0 and 1 for the fraction of specularity. '
        'Specularity fractions greater than 0.1 are not realistic for non-metallic '
        'materials.'
    )

    roughness: float = Field(
        default=0,
        ge=0,
        le=1,
        description='A value between 0 and 1 for the roughness, specified as the '
        'RMS slope of surface facets. Roughness greater than 0.2 are not realistic.'
    )


class Metal(Plastic):
    """Radiance metal material."""

    type: constr(regex='^Metal$') = 'Metal'

    specularity: float = Field(
        default=0.9,
        ge=0,
        le=1,
        description='A value between 0 and 1 for the fraction of specularity. '
        'Specularity fractions lower than 0.9 are not realistic for metallic materials.'
    )


class Trans(Plastic):
    """Radiance Translucent material."""

    type: constr(regex='^Trans$') = 'Trans'

    transmitted_diff: float = Field(
        default=0,
        ge=0,
        le=1,
        description='The fraction of transmitted light that is transmitted diffusely in '
        'a scattering fashion.'
    )

    transmitted_spec: float = Field(
        default=0,
        ge=0,
        le=1,
        description='The fraction of transmitted light that is not diffusely scattered.'
    )


class Glass(ModifierBase):
    """Radiance glass material."""

    type: constr(regex='^Glass$') = 'Glass'

    modifier: Optional[_REFERENCE_UNION_MODIFIERS] = Field(
        default=Void(),
        description='Material modifier.'
    )

    dependencies: List[_REFERENCE_UNION_MODIFIERS] = Field(
        default=None,
        description='List of modifiers that this modifier depends on. This argument '
        'is only useful for defining advanced modifiers where the modifier is '
        'defined based on other modifiers.'
    )

    r_transmissivity: float = Field(
        default=0.0,
        ge=0,
        le=1,
        description='A value between 0 and 1 for the red channel transmissivity.'
    )

    g_transmissivity: float = Field(
        default=0.0,
        ge=0,
        le=1,
        description='A value between 0 and 1 for the green channel transmissivity.'
    )

    b_transmissivity: float = Field(
        default=0.0,
        ge=0,
        le=1,
        description='A value between 0 and 1 for the blue channel transmissivity.'
    )

    refraction_index: Optional[float] = Field(
        default=1.52,
        gt=1,
        description='A value greater than 1 for the index of refraction. Typical '
        'values are 1.52 for float glass and 1.4 for ETFE.'
    )


class BSDF(ModifierBase):
    """Radiance BSDF (Bidirectional Scattering Distribution Function) material."""

    type: constr(regex='^BSDF$') = 'BSDF'

    modifier: Optional[_REFERENCE_UNION_MODIFIERS] = Field(
        default=Void(),
        description='Material modifier.'
    )

    dependencies: List[_REFERENCE_UNION_MODIFIERS] = Field(
        default=None,
        description='List of modifiers that this modifier depends on. This argument '
        'is only useful for defining advanced modifiers where the modifier is defined '
        'based on other modifiers.'
    )

    up_orientation: List[float] = Field(
        default=(0.01, 0.01, 1.00),
        min_items=3,
        max_items=3,
        description='Vector as sequence that sets the hemisphere that the BSDF '
        'material faces.'
    )

    thickness: float = Field(
        default=0,
        description='Optional number to set the thickness of the BSDF material '
        'Sign of thickness indicates whether proxied geometry is behind the BSDF '
        'surface (when thickness is positive) or in front (when thickness is '
        'negative).'
    )

    function_file: str = Field(
        default='.',
        min_length=1,
        max_length=100,
        description='Optional input for function file. Using "." will ensure that '
        'BSDF data is written to the root of wherever a given study is run.'
    )

    transform: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='Optional transform input to scale the thickness and reorient '
        'the up vector.'
    )

    bsdf_data: str = Field(
        ...,
        description='A string with the contents of the BSDF XML file.'
    )

    front_diffuse_reflectance: List[float] = Field(
        default=None,
        min_items=3,
        max_items=3,
        description='Optional additional front diffuse reflectance as sequence of '
        'three RGB numbers.'
    )

    back_diffuse_reflectance: List[float] = Field(
        default=None,
        min_items=3,
        max_items=3,
        description='Optional additional back diffuse reflectance as sequence of '
        'three RGB numbers.'
    )

    diffuse_transmittance: List[float] = Field(
        default=None,
        min_items=3,
        max_items=3,
        description='Optional additional diffuse transmittance as sequence of '
        'three RGB numbers.'
    )

    @validator('front_diffuse_reflectance')
    def check_front_diff_value(cls, values):
        """Ensure every list value is between 0 and 1."""
        assert all(0 <= v <= 1 for v in values), \
            'Every value in front diffuse reflectance must be between 0 and 1.'
        return values

    @validator('back_diffuse_reflectance')
    def check_back_diff_value(cls, values):
        """Ensure every list value is between 0 and 1."""
        assert all(0 <= v <= 1 for v in values), \
            'Every value in back diffuse reflectance must be between 0 and 1.'
        return values

    @validator('diffuse_transmittance')
    def check_diff_trans_value(cls, values):
        """Ensure every list value is between 0 and 1."""
        assert all(0 <= v <= 1 for v in values), \
            'Every value in diffuse transmittance must be between 0 and 1.'
        return values


class Light(ModifierBase):
    """Radiance Light material."""

    type: constr(regex='^Light$') = 'Light'

    modifier: Optional[_REFERENCE_UNION_MODIFIERS] = Field(
        default=Void(),
        description='Material modifier.'
    )

    dependencies: List[_REFERENCE_UNION_MODIFIERS] = Field(
        default=None,
        description='List of modifiers that this modifier depends on. This argument '
        'is only useful for defining advanced modifiers where the modifier is '
        'defined based on other modifiers.'
    )

    r_emittance: float = Field(
        default=0.0,
        ge=0,
        le=1,
        description='A value between 0 and 1 for the red channel of the modifier.'
    )

    g_emittance: float = Field(
        default=0.0,
        ge=0,
        le=1,
        description='A value between 0 and 1 for the green channel of the modifier.'
    )

    b_emittance: float = Field(
        default=0.0,
        ge=0,
        le=1,
        description='A value between 0 and 1 for the blue channel of the modifier.'
    )


class Glow(Light):
    """Radiance Glow material."""

    type: constr(regex='^Glow$') = 'Glow'

    max_radius: float = Field(
        default=0,
        description='Maximum radius for shadow testing. Objects with zero radius '
        'are permissable and may participate in interreflection calculation (though '
        'they are not representative of real light sources). Negative values will '
        'never contribute to scene illumination.'
    )


# Union Modifier Schema objects defined for type reference
_REFERENCE_UNION_MODIFIERS = \
    Union[Plastic, Glass, BSDF, Glow, Light, Trans, Metal, Void, Mirror]

# Required for self.referencing model
# see https://pydantic-docs.helpmanual.io/#self-referencing-models
Mirror.update_forward_refs()
Plastic.update_forward_refs()
Glass.update_forward_refs()
BSDF.update_forward_refs()
Glow.update_forward_refs()
Light.update_forward_refs()
Trans.update_forward_refs()
Metal.update_forward_refs()
Void.update_forward_refs()
