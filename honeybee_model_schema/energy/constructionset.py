"""ConstructionSet Schema"""
from pydantic import BaseModel, Schema, validator
from enum import Enum


class WallSetAbridged(BaseModel):
    """A set of constructions for wall assemblies."""

    type: Enum('WallSetAbridged', {
               'type': 'WallSetAbridged'})

    interior_construction: str = Schema(
        default=None,
        min_length=1,
        max_length=100
    )

    exterior_construction: str = Schema(
        default=None,
        min_length=1,
        max_length=100
    )

    ground_construction: str = Schema(
        default=None,
        min_length=1,
        max_length=100
    )


class FloorSetAbridged(BaseModel):
    """A set of constructions for floor assemblies."""

    type: Enum('FloorSetAbridged', {
               'type': 'FloorSetAbridged'})

    interior_construction: str = Schema(
        default=None,
        min_length=1,
        max_length=100
    )

    exterior_construction: str = Schema(
        default=None,
        min_length=1,
        max_length=100
    )

    ground_construction: str = Schema(
        default=None,
        min_length=1,
        max_length=100
    )


class RoofCeilingSetAbridged(BaseModel):
    """A set of constructions for roof and ceiling assemblies."""

    type: Enum('RoofCeilingSetAbridged', {
               'type': 'RoofCeilingSetAbridged'})

    interior_construction: str = Schema(
        default=None,
        min_length=1,
        max_length=100
    )

    exterior_construction: str = Schema(
        default=None,
        min_length=1,
        max_length=100
    )

    ground_construction: str = Schema(
        default=None,
        min_length=1,
        max_length=100
    )


class ApertureSetAbridged(BaseModel):
    """A set of constructions for aperture assemblies."""

    type: Enum('ApertureSetAbridged', {
               'type': 'ApertureSetAbridged'})

    interior_construction: str = Schema(
        default=None,
        min_length=1,
        max_length=100
    )

    window_construction: str = Schema(
        default=None,
        min_length=1,
        max_length=100
    )

    skylight_construction: str = Schema(
        default=None,
        min_length=1,
        max_length=100
    )

    operable_construction: str = Schema(
        default=None,
        min_length=1,
        max_length=100
    )


class DoorSetAbridged(BaseModel):
    """A set of constructions for door assemblies."""

    type: Enum('DoorSetAbridged', {
               'type': 'DoorSetAbridged'})

    interior_construction: str = Schema(
        default=None,
        min_length=1,
        max_length=100
    )

    exterior_construction: str = Schema(
        default=None,
        min_length=1,
        max_length=100
    )

    overhead_construction: str = Schema(
        default=None,
        min_length=1,
        max_length=100
    )

    exterior_glass_construction: str = Schema(
        default=None,
        min_length=1,
        max_length=100
    )

    interior_glass_construction: str = Schema(
        default=None,
        min_length=1,
        max_length=100
    )


class ConstructionSetAbridged(BaseModel):
    """A set of constructions for different surface types and boundary conditions."""

    type: Enum('ConstructionSetAbridged', {
               'type': 'ConstructionSetAbridged'})

    name: str = Schema(
        ...,
        min_length=1,
        max_length=100
    )

    @validator('name')
    def check_name(cls, v):
        assert all(ord(i) < 128 for i in v), 'Name contains non ASCII characters.'
        assert all(char not in v for char in (',', ';', '!', '\n', '\t')), \
            'Name contains invalid character for EnergyPlus (, ; ! \n \t).'
        assert len(v) > 0, 'Name is an empty string.'
        assert len(v) <= 100, 'Number of characters must be less than 100.'

    wall_set: WallSetAbridged = Schema(
        default=None
    )

    floor_set: FloorSetAbridged = Schema(
        default=None
    )

    roof_ceiling_set: RoofCeilingSetAbridged = Schema(
        default=None
    )

    aperture_set: ApertureSetAbridged = Schema(
        default=None
    )

    door_set: DoorSetAbridged = Schema(
        default=None
    )

    shade_construction: str = Schema(
        default=None,
        min_length=1,
        max_length=100
    )


if __name__ == '__main__':
    print(ConstructionSetAbridged.schema_json(indent=2))
