from pydantic import Field, constr
from typing import List

from .._base import NoExtraBaseModel


class DaylightingControl(NoExtraBaseModel):

    type: constr(regex='^DaylightingControl$') = 'DaylightingControl'

    sensor_position: List[float] = Field(
        ...,
        description='A point as 3 (x, y, z) values for the position of the daylight '
        'sensor within the parent Room. This point should lie within the Room '
        'volume in order for the results to be meaningful.',
        min_items=3,
        max_items=3
    )

    illuminance_setpoint: float = Field(
        300,
        gt=0,
        description='A number for the illuminance setpoint in lux beyond '
        'which electric lights are dimmed if there is sufficient daylight.'
    )

    control_fraction: float = Field(
        1,
        ge=0,
        le=1,
        description='A number between 0 and 1 that represents the fraction of '
        'the Room lights that are dimmed when the illuminance at the sensor '
        'position is at the specified illuminance. 1 indicates that all lights are '
        'dim-able while 0 indicates that no lights are dim-able. Deeper rooms '
        'should have lower control fractions to account for the face that the '
        'lights in the back of the space do not dim in response to suitable '
        'daylight at the front of the room.'
    )

    min_power_input: float = Field(
        0.3,
        ge=0,
        le=1,
        description='A number between 0 and 1 for the the lowest power the '
        'lighting system can dim down to, expressed as a fraction of maximum '
        'input power.'
    )

    min_light_output: float = Field(
        0.2,
        ge=0,
        le=1,
        description='A number between 0 and 1 the lowest lighting output the '
        'lighting system can dim down to, expressed as a fraction of maximum '
        'light output.'
    )

    off_at_minimum: bool = Field(
        default=False,
        description='Boolean to note whether lights should switch off completely '
        'when they get to the minimum power input.'
    )
