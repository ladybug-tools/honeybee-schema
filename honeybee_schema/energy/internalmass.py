"""Programtype Schema"""
from pydantic import Field, constr

from ._base import IDdEnergyBaseModel


class InternalMassAbridged(IDdEnergyBaseModel):

    type: constr(regex='^InternalMassAbridged$') = 'InternalMassAbridged'

    construction: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description='Identifier for an OpaqueConstruction that represents the '
        'material that the internal thermal mass is composed of.'
    )

    area: float = Field(
        ...,
        gt=0,
        description='A number representing the surface area of the internal mass that '
        'is exposed to the Room air. This value should always be in square '
        'meters regardless of what units system the parent model is a part of.'
    )
