"""Boundary condition schemas."""
from pydantic import Field, constr
from typing import List, Union

from ._base import NoExtraBaseModel
from .altnumber import Autocalculate


class Outdoors(NoExtraBaseModel):

    type: constr(regex='^Outdoors$') = 'Outdoors'

    sun_exposure: bool = Field(
        True,
        description='A boolean noting whether the boundary is exposed to sun.'
    )

    wind_exposure: bool = Field(
        True,
        description='A boolean noting whether the boundary is exposed to wind.'
    )

    view_factor: Union[Autocalculate, float] = Field(
        Autocalculate(),
        ge=0,
        le=1,
        description='A number for the view factor to the ground. This can also be '
        'an Autocalculate object to have the view factor automatically calculated.'
    )


class Surface(NoExtraBaseModel):

    type: constr(regex='^Surface$') = 'Surface'

    boundary_condition_objects: List[str] = Field(
        ...,
        min_items=2,
        max_items=3,
        description='A list of up to 3 object identifiers that are adjacent to this one.'
        ' The first object is always the one that is immediately adjacent and is of '
        'the same object type (Face, Aperture, Door). When this boundary condition '
        'is applied to a Face, the second object in the tuple will be the parent '
        'Room of the adjacent object. When the boundary condition is applied to a '
        'sub-face (Door or Aperture), the second object will be the parent Face '
        'of the adjacent sub-face and the third object will be the parent Room '
        'of the adjacent sub-face.'
    )


class Ground(NoExtraBaseModel):

    type: constr(regex='^Ground$') = 'Ground'


class Adiabatic(NoExtraBaseModel):

    type: constr(regex='^Adiabatic$') = 'Adiabatic'


class OtherSideTemperature(NoExtraBaseModel):

    type: constr(regex='^OtherSideTemperature$') = 'OtherSideTemperature'

    heat_transfer_coefficient: float = Field(
        0,
        ge=0,
        description='A value in W/m2-K to indicate the combined convective/radiative '
        'film coefficient. If equal to 0, then the specified temperature above is '
        'equal to the exterior surface temperature. Otherwise, the temperature above '
        'is considered the outside air temperature and this coefficient is used to '
        'determine the difference between this outside air temperature and the '
        'exterior surface temperature.'
    )

    temperature: Union[Autocalculate, float] = Field(
        Autocalculate(),
        description='A temperature value in Celsius to note the temperature on the '
        'other side of the object. This input can also be an Autocalculate object '
        'to signify that the temperature is equal to the outdoor air temperature.'
    )
