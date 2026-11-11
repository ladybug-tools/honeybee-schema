"""Schema for project information."""
from typing import List, Union, Literal
from pydantic import BaseModel, Field, AnyUrl

from .energy.simulation import EfficiencyStandards, ClimateZones, BuildingTypes, Location


class ProjectInfo(BaseModel):
    """Project information."""

    type: Literal['ProjectInfo'] = 'ProjectInfo'

    north: float = Field(
        0,
        description='A number between -360 to 360 where positive values rotate the '
        'compass counterclockwise (towards the West) and negative values rotate the '
        'compass clockwise (towards the East).',
        le=360, ge=-360
    )

    weather_urls: Union[List[AnyUrl], None] = Field(
        None,
        description='A list of URLs to zip files that includes EPW, DDY and STAT files. '
        'You can find these URLs from the EPWMAP. The first URL will be used as the '
        'primary weather file.'
    )

    location: Union[Location, None] = Field(
        None,
        description='Project location. This value is usually generated from the '
        'information in the weather files.'
    )

    ashrae_climate_zone: Union[ClimateZones, None] = Field(
        None,
        description='Project location climate zone.'
    )

    building_type: Union[List[BuildingTypes], None] = Field(
        None,
        description='A list of building types for the project. The first building '
        'type is considered the primary type for the project.'
    )

    vintage: Union[List[EfficiencyStandards], None] = Field(
        None,
        description='A list of building vintages (e.g. ASHRAE_2019, ASHRAE_2016).'
    )
