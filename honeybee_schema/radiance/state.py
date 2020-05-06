"""State Schema"""

from pydantic import Field, constr
from typing import List
from .._base import NoExtraBaseModel, IDdBaseModel

from ..geometry import Face3D


class StateGeometryAbridged(IDdBaseModel):
    """StateGeometryAbridged represents shading for States."""

    type: constr(regex='^StateGeometryAbridged$') = 'StateGeometryAbridged'

    modifier: str = Field(
        default=None,
        description='A string for a Honeybee Radiance Modifier (default: None).'
        )

    modifier_blk: str = Field(
        default=None,
        description='A string for a Honeybee Radiance Modifier to be used '
                    'in direct solar simulations and in isolation studies (assessing'
                    'the contribution of individual objects) (default: None).'
        )

    geometry: Face3D = Field(
        ...,
        description='Planar Face3D for the geometry.'
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

    shades: List[StateGeometryAbridged] = Field(
        default=None,
        description='A list of StateGeometryAbridged objects (default: None).'
    )


class RadianceSubFaceStateAbridged(_RadianceStateBaseAbridged):
    """RadianceSubFaceStateAbridged is an abridged state for a dynamic Aperture or Door.
    """

    type: constr(regex='^RadianceSubFaceStateAbridged$') = 'RadianceSubFaceStateAbridged'

    shades: List[StateGeometryAbridged] = Field(
        default=None,
        description='A list of StateGeometryAbridged objects (default: None).'
    )

    vmtx_geometry: Face3D = Field(
        default=None,
        description='A Face3D for the view matrix geometry (default: None).'
    )

    dmtx_geometry: Face3D = Field(
        default=None,
        description='A Face3D for the daylight matrix geometry (default: None).'
    )

