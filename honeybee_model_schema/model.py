"""Model schema and the 5 geometry objects that define it."""
from pydantic import BaseModel, Schema, validator, constr
from typing import List, Union
from enum import Enum

from ._base import NamedBaseModel
from .bc import Outdoors, Surface, Ground, Adiabatic
from .energy.properties import ShadeEnergyPropertiesAbridged, \
    DoorEnergyPropertiesAbridged, ApertureEnergyPropertiesAbridged, \
    FaceEnergyPropertiesAbridged, RoomEnergyPropertiesAbridged, \
    ModelEnergyProperties


class Plane(BaseModel):

    n: List[float] = Schema(
        ...,
        description="Plane normal as 3 (x, y, z) values.",
        minItems=3,
        maxItems=3
    )

    o: List[float] = Schema(
        ...,
        description="Plane origin as 3 (x, y, z) values",
        minItems=3,
        maxItems=3
    )

    x: List[float] = Schema(
        default=None,
        description="Plane x-axis as 3 (x, y, z) values",
        minItems=3,
        maxItems=3
    )


class Face3D(BaseModel):
    """A single planar face in 3D space."""

    type: Enum('Face3D', {'type': 'Face3D'})

    boundary: List[List[float]] = Schema(
        ...,
        description='A list of points representing the outer boundary vertices of '
            'the face. The list should include at least 3 points and each point '
            'should be a list of 3 (x, y, z) values.'
    )

    holes: List[List[List[float]]] = Schema(
        default=None,
        description='Optional list of lists with one list for each hole in the face.'
            'Each hole should be a list of at least 3 points and each point a list '
            'of 3 (x, y, z) values. If None, it will be assumed that there are no '
            'holes in the face.'
    )

    plane: Plane = Schema(
        default=None,
        description='Optional Plane indicating the plane in which the face exists.'
            'If None, the plane will usually be derived from the boundary points.'
    )

    @validator('boundary', whole=True)
    def check_num_items(cls, v):
        for i in v:
            if len(i) != 3:
                raise ValueError(
                    'Number of floats must be 3 for (x, y, z).'
                )
        return v

    @validator('holes', whole=True)
    def check_num_items_holes(cls, v):
        for pt_list in v:
            for pt in pt_list:
                if len(pt) != 3:
                    raise ValueError(
                        'Number of floats must be 3 for (x, y, z).'
                    )
        return v


class ShadePropertiesAbridged(BaseModel):

    type: Enum('ShadePropertiesAbridged', {'type': 'ShadePropertiesAbridged'})

    energy: ShadeEnergyPropertiesAbridged = Schema(
        default=None
    )


class Shade(NamedBaseModel):

    type: Enum('Shade', {'type': 'Shade'})

    geometry: Face3D = Schema(
        ...,
        description='Planar Face3D for the geometry.'
    )

    properties: ShadePropertiesAbridged = Schema(
        ...,
        description='Extension properties for particular simulation engines '
            '(Radiance, EnergyPlus).'
    )


class DoorPropertiesAbridged(BaseModel):

    type: Enum('DoorPropertiesAbridged', {'type': 'DoorPropertiesAbridged'})

    energy: DoorEnergyPropertiesAbridged = Schema(
        default=None
    )


class Door(NamedBaseModel):

    type: Enum('Door', {'type': 'Door'})

    geometry: Face3D = Schema(
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

    is_glass: bool = Schema(
        False,
        description='Boolean to note whether this object is a glass door as opposed '
            'to an opaque door.'
    )

    properties: DoorPropertiesAbridged = Schema(
        ...,
        description='Extension properties for particular simulation engines '
            '(Radiance, EnergyPlus).'
    )


class AperturePropertiesAbridged(BaseModel):

    type: Enum('AperturePropertiesAbridged', {
               'type': 'AperturePropertiesAbridged'})

    energy: ApertureEnergyPropertiesAbridged = Schema(
        default=None
    )


class Aperture(NamedBaseModel):

    type: Enum('Aperture', {'type': 'Aperture'})

    geometry: Face3D = Schema(
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

    is_operable: bool = Schema(
        False,
        description='Boolean to note whether the Aperture can be opened for ventilation.'
    )

    indoor_shades: List[Shade] = Schema(
        default=None,
        description='Shades assigned to the interior side of this object '
            '(eg. window sill, light shelf).'
    )

    outdoor_shades: List[Shade] = Schema(
        default=None,
        description='Shades assigned to the exterior side of this object '
            '(eg. mullions, louvers).'
    )

    properties: AperturePropertiesAbridged = Schema(
        ...,
        description='Extension properties for particular simulation engines '
            '(Radiance, EnergyPlus).'
    )


class FacePropertiesAbridged(BaseModel):

    type: Enum('FacePropertiesAbridged', {'type': 'FacePropertiesAbridged'})

    energy: FaceEnergyPropertiesAbridged = Schema(
        default=None
    )


class FaceType(str, Enum):

    wall = 'Wall'
    floor = 'Floor'
    roof_ceiling = 'RoofCeiling'
    air_wall = 'AirWall'


class Face(NamedBaseModel):

    type: Enum('Face', {'type': 'Face'})

    geometry: Face3D = Schema(
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

    apertures: List[Aperture] = Schema(
        default=None,
        description='Apertures assigned to this Face. Should be coplanar with this '
            'Face and completely within the boundary of the Face to be valid.'
    )

    doors: List[Door] = Schema(
        default=None,
        description='Doors assigned to this Face. Should be coplanar with this '
            'Face and completely within the boundary of the Face to be valid.'
    )

    indoor_shades: List[Shade] = Schema(
        default=None,
        description='Shades assigned to the interior side of this object.'
    )

    outdoor_shades: List[Shade] = Schema(
        default=None,
        description='Shades assigned to the exterior side of this object '
            '(eg. balcony, overhang).'
    )

    properties: FacePropertiesAbridged = Schema(
        ...,
        description='Extension properties for particular simulation engines '
            '(Radiance, EnergyPlus).'
    )


class RoomPropertiesAbridged(BaseModel):

    type: Enum('RoomPropertiesAbridged', {'type': 'RoomPropertiesAbridged'})

    energy: RoomEnergyPropertiesAbridged


class Room(NamedBaseModel):

    type: Enum('Room', {'type': 'Room'})

    faces: List[Face] = Schema(
        ...,
        min_items=4,
        description='Faces that together form the closed volume of a room.'
    )

    indoor_shades:  List[Shade] = Schema(
        default=None,
        description='Shades assigned to the interior side of this object '
            '(eg. partitions, tables).'
    )

    outdoor_shades: List[Shade] = Schema(
        default=None,
        description='Shades assigned to the exterior side of this object '
            '(eg. trees, landscaping).'
    )

    properties: RoomPropertiesAbridged = Schema(
        ...,
        description='Extension properties for particular simulation engines '
            '(Radiance, EnergyPlus).'
    )


class ModelProperties(BaseModel):

    type: Enum('ModelProperties', {'type': 'ModelProperties'})

    energy: ModelEnergyProperties


class Model(NamedBaseModel):

    type: Enum('Model', {'type': 'Model'})

    rooms: List[Room] = Schema(
        default=None,
        description='A list of Rooms in the model.'
    )

    orphaned_faces: List[Face] = Schema(
        default=None,
        description='A list of Faces in the model that lack a parent Room. Note that '
            'orphaned Faces are not acceptable for Models that are to be exported '
            'for energy simulation.'
    )

    orphaned_shades: List[Shade] = Schema(
        default=None,
        description='A list of Shades in the model that lack a parent.'
    )

    orphaned_apertures: List[Aperture] = Schema(
        default=None,
        description='A list of Apertures in the model that lack a parent Face. '
            'Note that orphaned Apertures are not acceptable for Models that are '
            'to be exported for energy simulation.'
    )

    orphaned_doors: List[Door] = Schema(
        default=None,
        description='A list of Doors in the model that lack a parent Face. '
            'Note that orphaned Doors are not acceptable for Models that are '
            'to be exported for energy simulation.'
    )

    north_angle: float = Schema(
        default=0,
        ge=0,
        lt=360,
        description='The clockwise north direction in degrees.'
    )

    properties: ModelProperties = Schema(
        ...,
        description='Extension properties for particular simulation engines '
            '(Radiance, EnergyPlus).'
    )


if __name__ == '__main__':
    print(Model.schema_json(indent=2))
