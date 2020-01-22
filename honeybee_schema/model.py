"""Model schema and the 5 geometry objects that define it."""
from pydantic import BaseModel, Field, validator, constr, conlist
from typing import List, Union
from enum import Enum

from ._base import NamedBaseModel
from .bc import Outdoors, Surface, Ground, Adiabatic
from .energy.properties import ShadeEnergyPropertiesAbridged, \
    DoorEnergyPropertiesAbridged, ApertureEnergyPropertiesAbridged, \
    FaceEnergyPropertiesAbridged, RoomEnergyPropertiesAbridged, \
    ModelEnergyProperties


class Plane(BaseModel):

    type: constr(regex='^Plane$') = 'Plane'

    n: List[float] = Field(
        ...,
        description="Plane normal as 3 (x, y, z) values.",
        min_items=3,
        max_items=3
    )

    o: List[float] = Field(
        ...,
        description="Plane origin as 3 (x, y, z) values",
        min_items=3,
        max_items=3
    )

    x: List[float] = Field(
        default=None,
        description="Plane x-axis as 3 (x, y, z) values. If None, it is autocalculated.",
        min_items=3,
        max_items=3
    )


class Face3D(BaseModel):
    """A single planar face in 3D space."""

    type: constr(regex='^Face3D$') = 'Face3D'

    boundary: List[conlist(float, min_items=3, max_items=3)] = Field(
        ...,
        min_items=3,
        description='A list of points representing the outer boundary vertices of '
            'the face. The list should include at least 3 points and each point '
            'should be a list of 3 (x, y, z) values.'
    )

    holes: List[conlist(conlist(float, min_items=3, max_items=3), min_items=3)] = Field(
        default=None,
        description='Optional list of lists with one list for each hole in the face.'
            'Each hole should be a list of at least 3 points and each point a list '
            'of 3 (x, y, z) values. If None, it will be assumed that there are no '
            'holes in the face.'
    )

    plane: Plane = Field(
        default=None,
        description='Optional Plane indicating the plane in which the face exists.'
            'If None, the plane will usually be derived from the boundary points.'
    )


class ShadePropertiesAbridged(BaseModel):

    type: constr(regex='^ShadePropertiesAbridged$') = 'ShadePropertiesAbridged'

    energy: ShadeEnergyPropertiesAbridged = Field(
        default=None
    )


class Shade(NamedBaseModel):

    type: constr(regex='^Shade$') = 'Shade'

    geometry: Face3D = Field(
        ...,
        description='Planar Face3D for the geometry.'
    )

    properties: ShadePropertiesAbridged = Field(
        ...,
        description='Extension properties for particular simulation engines '
            '(Radiance, EnergyPlus).'
    )


class DoorPropertiesAbridged(BaseModel):

    type: constr(regex='^DoorPropertiesAbridged$') = 'DoorPropertiesAbridged'

    energy: DoorEnergyPropertiesAbridged = Field(
        default=None
    )


class Door(NamedBaseModel):

    type: constr(regex='^Door$') = 'Door'

    geometry: Face3D = Field(
        ...,
        description='Planar Face3D for the geometry.'
    )

    boundary_condition: Union[Outdoors, Surface]

    @validator('boundary_condition')
    def suface_bc_objects(cls, v):
        if v.type == 'Surface':
            assert len(v.boundary_condition_objects) == 3, 'Door Surface boundary ' \
                'condition must have 3 boundary_condition_objects.'
        return v

    is_glass: bool = Field(
        False,
        description='Boolean to note whether this object is a glass door as opposed '
            'to an opaque door.'
    )

    properties: DoorPropertiesAbridged = Field(
        ...,
        description='Extension properties for particular simulation engines '
            '(Radiance, EnergyPlus).'
    )


class AperturePropertiesAbridged(BaseModel):

    type: constr(regex='^AperturePropertiesAbridged$') = 'AperturePropertiesAbridged'

    energy: ApertureEnergyPropertiesAbridged = Field(
        default=None
    )


class Aperture(NamedBaseModel):

    type: constr(regex='^Aperture$') = 'Aperture'

    geometry: Face3D = Field(
        ...,
        description='Planar Face3D for the geometry.'
    )

    boundary_condition: Union[Outdoors, Surface]

    @validator('boundary_condition')
    def suface_bc_objects(cls, v):
        if v.type == 'Surface':
            assert len(v.boundary_condition_objects) == 3, 'Aperture Surface boundary ' \
                'condition must have 3 boundary_condition_objects.'
        return v

    is_operable: bool = Field(
        False,
        description='Boolean to note whether the Aperture can be opened for ventilation.'
    )

    indoor_shades: List[Shade] = Field(
        default=None,
        description='Shades assigned to the interior side of this object '
            '(eg. window sill, light shelf).'
    )

    outdoor_shades: List[Shade] = Field(
        default=None,
        description='Shades assigned to the exterior side of this object '
            '(eg. mullions, louvers).'
    )

    properties: AperturePropertiesAbridged = Field(
        ...,
        description='Extension properties for particular simulation engines '
            '(Radiance, EnergyPlus).'
    )


class FacePropertiesAbridged(BaseModel):

    type: constr(regex='^FacePropertiesAbridged$') = 'FacePropertiesAbridged'

    energy: FaceEnergyPropertiesAbridged = Field(
        default=None
    )


class FaceType(str, Enum):

    wall = 'Wall'
    floor = 'Floor'
    roof_ceiling = 'RoofCeiling'
    air_wall = 'AirWall'


class Face(NamedBaseModel):

    type: constr(regex='^Face$') = 'Face'

    geometry: Face3D = Field(
        ...,
        description='Planar Face3D for the geometry.'
    )

    face_type: FaceType

    boundary_condition: Union[Ground, Outdoors, Adiabatic, Surface]

    @validator('boundary_condition')
    def suface_bc_objects(cls, v):
        if v.type == 'Surface':
            assert len(v.boundary_condition_objects) == 2, 'Face Surface boundary ' \
                'condition must have 2 boundary_condition_objects.'
        return v

    apertures: List[Aperture] = Field(
        default=None,
        description='Apertures assigned to this Face. Should be coplanar with this '
            'Face and completely within the boundary of the Face to be valid.'
    )

    doors: List[Door] = Field(
        default=None,
        description='Doors assigned to this Face. Should be coplanar with this '
            'Face and completely within the boundary of the Face to be valid.'
    )

    indoor_shades: List[Shade] = Field(
        default=None,
        description='Shades assigned to the interior side of this object.'
    )

    outdoor_shades: List[Shade] = Field(
        default=None,
        description='Shades assigned to the exterior side of this object '
            '(eg. balcony, overhang).'
    )

    properties: FacePropertiesAbridged = Field(
        ...,
        description='Extension properties for particular simulation engines '
            '(Radiance, EnergyPlus).'
    )


class RoomPropertiesAbridged(BaseModel):

    type: constr(regex='^RoomPropertiesAbridged$') = 'RoomPropertiesAbridged'

    energy: RoomEnergyPropertiesAbridged = Field(
        default=None
    )


class Room(NamedBaseModel):

    type: constr(regex='^Room$') = 'Room'

    faces: List[Face] = Field(
        ...,
        min_items=4,
        description='Faces that together form the closed volume of a room.'
    )

    indoor_shades: List[Shade] = Field(
        default=None,
        description='Shades assigned to the interior side of this object '
            '(eg. partitions, tables).'
    )

    outdoor_shades: List[Shade] = Field(
        default=None,
        description='Shades assigned to the exterior side of this object '
            '(eg. trees, landscaping).'
    )

    properties: RoomPropertiesAbridged = Field(
        ...,
        description='Extension properties for particular simulation engines '
            '(Radiance, EnergyPlus).'
    )

    multiplier: int = Field(
        1,
        ge=1,
        description='An integer noting how many times this Room is repeated. '
            'Multipliers are used to speed up the calculation when similar Rooms are '
            'repeated more than once. Essentially, a given simulation with the '
            'Room is run once and then the result is mutliplied by the multiplier.'
    )


class ModelProperties(BaseModel):

    type: constr(regex='^ModelProperties$') = 'ModelProperties'

    energy: ModelEnergyProperties = Field(
        default=None
    )


class Model(NamedBaseModel):

    type: constr(regex='^Model$') = 'Model'

    rooms: List[Room] = Field(
        default=None,
        description='A list of Rooms in the model.'
    )

    orphaned_faces: List[Face] = Field(
        default=None,
        description='A list of Faces in the model that lack a parent Room. Note that '
            'orphaned Faces are not acceptable for Models that are to be exported '
            'for energy simulation.'
    )

    orphaned_shades: List[Shade] = Field(
        default=None,
        description='A list of Shades in the model that lack a parent.'
    )

    orphaned_apertures: List[Aperture] = Field(
        default=None,
        description='A list of Apertures in the model that lack a parent Face. '
            'Note that orphaned Apertures are not acceptable for Models that are '
            'to be exported for energy simulation.'
    )

    orphaned_doors: List[Door] = Field(
        default=None,
        description='A list of Doors in the model that lack a parent Face. '
            'Note that orphaned Doors are not acceptable for Models that are '
            'to be exported for energy simulation.'
    )

    north_angle: float = Field(
        default=0,
        ge=0,
        lt=360,
        description='The clockwise north direction in degrees.'
    )

    properties: ModelProperties = Field(
        ...,
        description='Extension properties for particular simulation engines '
            '(Radiance, EnergyPlus).'
    )


if __name__ == '__main__':
    print(Model.schema_json(indent=2))
