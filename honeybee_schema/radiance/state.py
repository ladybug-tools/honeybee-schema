"""State Schema"""

from pydantic import Field, constr
from typing import List, Union
from .._base import NoExtraBaseModel

from ..model import Face3D
from .properties import _PropertiesBaseAbridged


class StateShade(_PropertiesBaseAbridged):
    """StateShade represents shading for States."""

    type: constr(regex='^StateShade$') = 'StateShade'

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

    shades: List[Union[StateShade]] = Field(
        default=None,
        description='A list of StateShade objects (default: None).'
    )


class RadianceSubFaceStateAbridged(_RadianceStateBaseAbridged):
    """RadianceSubFaceStateAbridged is an abridged state for a dynamic Aperture or Door.
    """

    type: constr(regex='^RadianceSubFaceStateAbridged$') = 'RadianceSubFaceStateAbridged'

    shades: List[Union[StateShade]] = Field(
        default=None,
        description='A list of StateShade objects (default: None).'
    )

    vmtx_geometry: Face3D = Field(
        default=None,
        description='A Face3D for the view matrix geometry (default: None).'
    )

    vmtx_geometry: Face3D = Field(
        default=None,
        description='A Face3D for the daylight matrix geometry (default: None).'
    )

