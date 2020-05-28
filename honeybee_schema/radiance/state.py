"""State Schema"""
from pydantic import Field, constr
from typing import List
from .._base import NoExtraBaseModel
from ._base import IDdRadianceBaseModel

from ..geometry import Face3D


class StateGeometryAbridged(IDdRadianceBaseModel):
    """A single planar geometry that can be assigned to Radiance states."""

    type: constr(regex='^StateGeometryAbridged$') = 'StateGeometryAbridged'

    modifier: str = Field(
        default=None,
        description='A string for a Honeybee Radiance Modifier identifier '
                    '(default: None).'
    )

    modifier_direct: str = Field(
        default=None,
        description='A string for Honeybee Radiance Modifier identifiers to be used '
                    'in direct solar simulations and in isolation studies (assessing'
                    'the contribution of individual objects) (default: None).'
    )

    geometry: Face3D = Field(
        ...,
        description='A ladybug_geometry Face3D.'
    )


class RadianceShadeStateAbridged(NoExtraBaseModel):
    """RadianceShadeStateAbridged represents a single state for a dynamic Shade."""

    type: constr(regex='^RadianceShadeStateAbridged$') = 'RadianceShadeStateAbridged'

    modifier: str = Field(
        default=None,
        description='A Radiance Modifier identifier (default: None).'
    )

    modifier_direct: str = Field(
        default=None,
        description='A Radiance Modifier identifier (default: None).'
    )

    shades: List[StateGeometryAbridged] = Field(
        default=None,
        description='A list of StateGeometryAbridged objects (default: None).'
    )


class RadianceSubFaceStateAbridged(RadianceShadeStateAbridged):
    """RadianceSubFaceStateAbridged is an abridged state for a dynamic Aperture or Door.
    """

    type: constr(regex='^RadianceSubFaceStateAbridged$') = 'RadianceSubFaceStateAbridged'

    vmtx_geometry: Face3D = Field(
        default=None,
        description='A Face3D for the view matrix geometry (default: None).'
    )

    dmtx_geometry: Face3D = Field(
        default=None,
        description='A Face3D for the daylight matrix geometry (default: None).'
    )
