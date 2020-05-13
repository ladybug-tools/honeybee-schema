"""SensorGrid and Sensor Schema"""
from pydantic import Field, constr
from typing import List
from enum import Enum
from .._base import NoExtraBaseModel
from ._base import IDdRadianceBaseModel


class Sensor(NoExtraBaseModel):
    """A single Radiance of sensors."""

    type: constr(regex='^Sensor$') = 'Sensor'

    pos: List[float] = Field(
        ...,
        description="Position of sensor in space as an array of (x, y, z) values.",
        min_items=3,
        max_items=3
    )

    dir: List[float] = Field(
        ...,
        description="Direction of sensor as an array of (x, y, z) values.",
        min_items=3,
        max_items=3
    )


class SensorGrid(IDdRadianceBaseModel):
    """A grid of sensors."""

    type: constr(regex='^SensorGrid$') = 'SensorGrid'

    sensors: List[Sensor] = Field(
        ...,
        description="A list of sensors that belong to the grid."
    )

    room_identifier: str = Field(
        None,
        regex=r'[A-Za-z0-9_-]',
        min_length=1,
        max_length=100,
        description='Optional text string for the Room identifier to which this '
        'SensorGrid belongs. This will be used to narrow down the number of '
        'aperture groups that have to be run with this sensor grid. If None, '
        'the grid will be run with all aperture groups in the model.'
    )

    light_path: List[List[str]] = Field(
        None,
        description='Get or set a list of lists for the light path from the grid to the '
        'sky. Each sub-list contains identifiers of aperture groups through which '
        'light passes. (eg. [["SouthWindow1"], ["static_apertures", "NorthWindow2"]]).'
        'Setting this property will override any auto-calculation of the light '
        'path from the model and room_identifier upon export to the simulation.'
    )


class ViewType(str, Enum):
    """A single character for the view type (-vt)."""
    perspective = 'v'
    hemispherical_fisheye = 'h'
    parallel = 'l'
    cylindrical_panorama = 'c'
    angular_fisheye = 'a'
    planisphere = 's'


class View(IDdRadianceBaseModel):
    """A single Radiance of sensors."""

    type: constr(regex='^View$') = 'View'

    position: List[float] = Field(
        ...,
        description='The view position (-vp) as an array of (x, y, z) values.'
        'This is the focal point of a perspective view or the center of a '
        'parallel projection.',
        min_items=3,
        max_items=3
    )

    direction: List[float] = Field(
        ...,
        description='The view direction (-vd) as an array of (x, y, z) values.'
            'The length of this vector indicates the focal distance as needed by '
            'the pixel depth of field (-pd) in rpict.',
        min_items=3,
        max_items=3
    )

    up_vector: List[float] = Field(
        ...,
        description='The view up (-vu) vector as an array of (x, y, z) values.',
        min_items=3,
        max_items=3
    )

    view_type: ViewType = ViewType.perspective

    h_size: float = Field(
        60,
        description='A number for the horizontal field of view in degrees (for '
        'all perspective projections including fisheye). For a parallel '
        'projection, this is the view width in world coordinates.'
    )

    v_size: float = Field(
        60,
        description='A number for the vertical field of view in degrees (for '
            'all perspective projections including fisheye). For a parallel '
            'projection, this is the view width in world coordinates.'
    )

    shift: float = Field(
        None,
        description='The view shift (-vs). This is the amount the actual '
        'image will be shifted to the right of the specified view. This '
        'option is useful for generating skewed perspectives or rendering '
        'an image a piece at a time. A value of 1 means that the rendered '
        'image starts just to the right of the normal view. A value of -1 '
        'would be to the left. Larger or fractional values are permitted '
        'as well.'
    )

    lift: float = Field(
        None,
        description='The view lift (-vl). This is the amount the actual '
        'image will be lifted up from the specified view. This '
        'option is useful for generating skewed perspectives or rendering '
        'an image a piece at a time. A value of 1 means that the rendered '
        'image starts just to the right of the normal view. A value of -1 '
        'would be to the left. Larger or fractional values are permitted '
        'as well.'
    )

    fore_clip: float = Field(
        None,
        description='View fore clip (-vo) at a distance from the view point.'
        'The plane will be perpendicular to the view direction for perspective '
        'and parallel view types. For fisheye view types, the clipping plane is '
        'actually a clipping sphere, centered on the view point with fore_clip radius. '
        'Objects in front of this imaginary surface will not be visible.'
    )

    aft_clip: float = Field(
        None,
        description='View aft clip (-va) at a distance from the view point.'
        'Like the view fore plane, it will be perpendicular to the view '
        'direction for perspective and parallel view types. For fisheye '
        'view types, the clipping plane is actually a clipping sphere, '
        'centered on the view point with radius val.'
    )

    room_identifier: str = Field(
        None,
        regex=r'[A-Za-z0-9_-]',
        min_length=1,
        max_length=100,
        description='Optional text string for the Room identifier to which this '
        'View belongs. This will be used to narrow down the number of aperture '
        'groups that have to be run with this sensor grid. If None, the grid '
        'will be run with all aperture groups in the model.'
    )

    light_path: List[List[str]] = Field(
        None,
        description='Get or set a list of lists for the light path from the view to the '
        'sky. Each sub-list contains identifiers of aperture groups through which '
        'light passes. (eg. [["SouthWindow1"], ["static_apertures", "NorthWindow2"]]).'
        'Setting this property will override any auto-calculation of the light '
        'path from the model and room_identifier upon export to the simulation.'
    )
