"""Model DOE-2 properties."""
from pydantic import Field, constr
from typing import Union

from .._base import NoExtraBaseModel
from ..altnumber import Autocalculate
from ..geometry import Face3D


class RoomDoe2Properties(NoExtraBaseModel):

    type: constr(regex='^RoomDoe2Properties$') = \
        'RoomDoe2Properties'

    assigned_flow: Union[Autocalculate, float] = Field(
        Autocalculate(),
        ge=0,
        description='A number for the design supply air flow rate for the zone '
        'the Room is assigned to (cfm). This establishes the minimum allowed '
        'design air flow. Note that the actual design flow may be larger. If '
        'Autocalculate, this parameter will not be written into the INP.'
    )

    flow_per_area: Union[Autocalculate, float] = Field(
        Autocalculate(),
        ge=0,
        description='A number for the design supply air flow rate to the zone '
        'per unit floor area (cfm/ft2). If Autocalculate, this parameter will '
        'not be written into the INP.'
    )

    min_flow_ratio: Union[Autocalculate, float] = Field(
        Autocalculate(),
        ge=0,
        le=1,
        description='A number between 0 and 1 for the minimum allowable zone '
        'air supply flow rate, expressed as a fraction of design flow rate. Applicable '
        'to variable-volume type systems only. If Autocalculate, this parameter will '
        'not be written into the INP.'
    )

    min_flow_per_area: Union[Autocalculate, float] = Field(
        Autocalculate(),
        ge=0,
        description='A number for the minimum air flow per square foot of '
        'floor area (cfm/ft2). This is an alternative way of specifying the '
        'min_flow_ratio. If Autocalculate, this parameter will not be written '
        'into the INP.'
    )

    hmax_flow_ratio: Union[Autocalculate, float] = Field(
        Autocalculate(),
        ge=0,
        le=1,
        description='A number between 0 and 1 for the ratio of the maximum (or fixed) '
        'heating airflow to the cooling airflow. The specific meaning varies according '
        'to the type of zone terminal. If Autocalculate, this parameter will '
        'not be written into the INP.'
    )

    space_polygon_geometry: Face3D = Field(
        default=None,
        description='An optional horizontal Face3D object, which will '
        'be used to set the SPACE polygon during export to INP. If None, '
        'the SPACE polygon is auto-calculated from the 3D Room geometry. '
        'Specifying a geometry here can help overcome some limitations of '
        'this auto-calculation, particularly for cases where the floors '
        'of the Room are composed of AirBoundaries.'
    )


class ModelDoe2Properties(NoExtraBaseModel):

    type: constr(regex='^ModelDoe2Properties$') = \
        'ModelDoe2Properties'
