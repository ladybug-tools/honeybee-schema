"""Geometry objects for model."""
from typing import List, Literal, Annotated, Union
from pydantic import Field
from ._base import NoExtraBaseModel


class Point3D(NoExtraBaseModel):
    """A point object in 3D space."""

    type: Literal['Point3D'] = 'Point3D'

    x: float = Field(
        ...,
        description='Number for X coordinate.'
    )

    y: float = Field(
        ...,
        description='Number for Y coordinate.'
    )

    z: float = Field(
        ...,
        description='Number for Z coordinate.'
    )


class LineSegment3D(NoExtraBaseModel):
    """A single line segment face in 3D space."""

    type: Literal['LineSegment3D'] = 'LineSegment3D'

    p: List[float] = Field(
        ...,
        description="Line segment base point as 3 (x, y, z) values.",
        min_length=3,
        max_length=3
    )

    v: List[float] = Field(
        ...,
        description="Line segment direction vector as 3 (x, y, z) values.",
        min_length=3,
        max_length=3
    )


class Plane(NoExtraBaseModel):

    type: Literal['Plane'] = 'Plane'

    n: List[float] = Field(
        ...,
        description="Plane normal as 3 (x, y, z) values.",
        min_length=3,
        max_length=3
    )

    o: List[float] = Field(
        ...,
        description="Plane origin as 3 (x, y, z) values",
        min_length=3,
        max_length=3
    )

    x: Union[List[float], None] = Field(
        default=None,
        description="Plane x-axis as 3 (x, y, z) values. If None, it is autocalculated.",
        min_length=3,
        max_length=3
    )


class Face3D(NoExtraBaseModel):
    """A single planar face in 3D space."""

    type: Literal['Face3D'] = 'Face3D'

    boundary: List[Annotated[List[float], Field(min_length=3, max_length=3)]] = Field(
        ...,
        min_length=3,
        description='A list of points representing the outer boundary vertices of '
        'the face. The list should include at least 3 points and each point '
        'should be a list of 3 (x, y, z) values.'
    )

    holes: Union[List[Annotated[List[Annotated[List[float], Field(min_length=3, max_length=3)]], Field(min_length=3)]], None] = Field(
        default=None,
        description='Optional list of lists with one list for each hole in the face.'
        'Each hole should be a list of at least 3 points and each point a list '
        'of 3 (x, y, z) values. If None, it will be assumed that there are no '
        'holes in the face.'
    )

    plane: Union[Plane, None] = Field(
        default=None,
        description='Optional Plane indicating the plane in which the face exists.'
        'If None, the plane will usually be derived from the boundary points.'
    )


class Color(NoExtraBaseModel):
    """A RGB color."""

    type: Literal['Color'] = 'Color'

    r: int = Field(
        ...,
        ge=0,
        le=255,
        description='Value for red channel.'
    )

    g: int = Field(
        ...,
        ge=0,
        le=255,
        description='Value for green channel.'
    )

    b: int = Field(
        ...,
        ge=0,
        le=255,
        description='Value for blue channel.'
    )

    a: int = Field(
        default=255,
        ge=0,
        le=255,
        description='Value for the alpha channel, which defines the opacity as a '
        'number between 0 (fully transparent) and 255 (fully opaque).'
    )


class Mesh3D(NoExtraBaseModel):
    """A mesh in 3D space."""

    type: Literal['Mesh3D'] = 'Mesh3D'

    vertices: List[Annotated[List[float], Field(min_length=3, max_length=3)]] = Field(
        ...,
        min_length=3,
        description='A list of points representing the vertices of the mesh. '
        'The list should include at least 3 points and each point '
        'should be a list of 3 (x, y, z) values.'
    )

    faces: List[Annotated[List[Annotated[int, Field(ge=0)]], Field(min_length=3, max_length=4)]] = Field(
        ...,
        min_length=1,
        description='A list of lists with each sub-list having either 3 or 4 '
        'integers. These integers correspond to indices within the list of vertices.'
    )

    colors: Union[List[Color], None] = Field(
        None,
        description='An optional list of colors that correspond to either the faces '
        'of the mesh or the vertices of the mesh.'
    )
