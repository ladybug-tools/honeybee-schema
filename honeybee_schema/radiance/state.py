"""State Schema"""
#from __future__ import absolute_import
from pprint import pprint as pp

from pydantic import Field, constr
from typing import List, Union
from .._base import NoExtraBaseModel
from .modifier import _REFERENCE_UNION_MODIFIERS

# TODO: Attempt at absolute import to avoid circular import errors
# from ..model import Face3D, Shade
import honeybee_schema.model
Face3D = honeybee_schema.model.Face3D
Shade = honeybee_schema.model.Shade

class _RadianceStateBase(NoExtraBaseModel):
    """Base model for Radiance State Schema"""

    modifier: _REFERENCE_UNION_MODIFIERS = Field(
        default=None,
        description='A Radiance Modifier object (default: None).'
    )

    modifier_direct: _REFERENCE_UNION_MODIFIERS = Field(
        default=None,
        description='A Radiance Modifier object (default: None).'
    )


class _RadianceStateBaseAbridged(NoExtraBaseModel):
    """Base model for abridge Radiance State Schema"""

    modifier: str = Field(
        default=None,
        description='A Radiance Modifier identifier (default: None).'
    )

    modifier_direct: str = Field(
        default=None,
        description='A Radiance Modifier identifier (default: None).'
    )


class RadianceShadeStateAbridged(_RadianceStateBaseAbridged):
    """RadianceShadeStateAbridged represents a single state for a dynamic Shade."""

    type: constr(regex='^RadianceShadeStateAbridged$') = 'RadianceShadeStateAbridged'

    shades: List[Union[Shade]] = Field(
        default=None,
        description='A list of ShadeAbridged object (default: None).'
    )


class RadianceShadeState(_RadianceStateBase):
    """RadianceShadeState is a single state for a dynamic Shade.
    """

    type: constr(regex='^RadianceShadeState$') = 'RadianceShadeState'

    shades: List[Union[Shade]] = Field(
        default=None,
        description='A list of Shade objects (default: None).'
    )


class RadianceSubFaceStateAbridged(_RadianceStateBaseAbridged):
    """RadianceSubFaceStateAbridged is an abridged state for a dynamic Aperture or Door.
    """

    type: constr(regex='^RadianceSubFaceStateAbridged$') = 'RadianceSubFaceStateAbridged'

    shades: List[Union[Shade]] = Field(
        default=None,
        description='A list of ShadeAbridged object (default: None).'
    )

    vmtx_geometry: Face3D = Field(
        default=None,
        description='A Face3D for the view matrix geometry (default: None).'
    )

    vmtx_geometry: Face3D = Field(
        default=None,
        description='A Face3D for the daylight matrix geometry (default: None).'
    )


class RadianceSubFaceState(_RadianceStateBase):
    """RadianceSubFaceState represents a single state ofr a dynamic Aperture or Door.
    """

    type: constr(regex='^RadianceSubFaceState$') = 'RadianceSubFaceState'

    shades: List[Union[Shade]] = Field(
        default=None,
        description='An optional list of Shade objects (default: None).'
    )

    vmtx_geometry: Face3D = Field(
        default=None,
        description='A Face3D for the view matrix geometry (default: None).'
    )

    vmtx_geometry: Face3D = Field(
        default=None,
        description='A Face3D for the daylight matrix geometry (default: None).'
    )
