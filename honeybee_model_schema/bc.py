"""Boundary condition schemas."""
from pydantic import BaseModel, Schema
from typing import List, Union
from enum import Enum


class Outdoors(BaseModel):

    type: Enum('Outdoors', {'type': 'Outdoors'})

    sun_exposure: bool = Schema(
        True,
        description='A boolean noting whether the boundary is exposed to sun.'
    )

    wind_exposure: bool = Schema(
        True,
        description='A boolean noting whether the boundary is exposed to wind.'
    )

    view_factor: Union[str, float] = Schema(
        'autocalculate',
        ge=0,
        le=1,
        description='A number for the view factor to the ground. This can also be '
            'the word "autocalculate" to have the view factor automatically calculated.'
    )

class Surface(BaseModel):

    type: Enum('Surface', {'type': 'Surface'})

    boundary_condition_objects: List[str] = Schema(
        ...,
        minItems=2,
        maxItems=3,
        description='A list of up to 3 object names that are adjacent to this one. '
            'The first object is always the one that is immediately adjacet and is of '
            'the same object type (Face, Aperture, Door). When this boundary condition '
            'is applied to a Face, the second object in the tuple will be the parent '
            'Room of the adjacent object. When the boundary condition is applied to a '
            'sub-face (Door or Aperture), the second object will be the parent Face '
            'of the adjacent sub-face and the third object will be the parent Room '
            'of the adjacent sub-face.'
    )


class Ground(BaseModel):

    type: Enum('Ground', {'type': 'Ground'})


class Adiabatic(BaseModel):

    type: Enum('Adiabatic', {'type': 'Adiabatic'})
