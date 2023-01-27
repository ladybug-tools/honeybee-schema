"""Detailed HVAC system schema defined using Ironbug."""
from pydantic import Field, constr
from .._base import IDdEnergyBaseModel


class DetailedHVAC(IDdEnergyBaseModel):
    """Detailed HVAC system object defined using IronBug or OpenStudio .NET bindings."""

    type: constr(regex='^DetailedHVAC$') = 'DetailedHVAC'

    specification: dict = Field(
        ...,
        description='A JSON-serializable dictionary representing the full '
        'specification of the detailed system. This can be obtained by calling '
        'the ToJson() method on any IronBug HVAC system and then serializing '
        'the resulting JSON string into a Python dictionary using the native '
        'Python json package. Note that the Rooms that the HVAC is assigned to '
        'must be specified as ThermalZones under this specification in order '
        'for the resulting Model this HVAC is a part of to be valid.'
    )
