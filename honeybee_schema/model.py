"""Model schema and the 5 geometry objects that define it."""
from pydantic import BaseModel, Field, validator, root_validator, constr, conlist
from typing import List, Union
from enum import Enum

from ._base import IDdBaseModel
from .boundarycondition import Outdoors, Surface, Ground, Adiabatic

from .energy.properties import ShadeEnergyPropertiesAbridged, \
    DoorEnergyPropertiesAbridged, ApertureEnergyPropertiesAbridged, \
    FaceEnergyPropertiesAbridged, RoomEnergyPropertiesAbridged, \
    ModelEnergyProperties

from .radiance.properties import ShadeRadiancePropertiesAbridged, \
    DoorRadiancePropertiesAbridged, ApertureRadiancePropertiesAbridged, \
    FaceRadiancePropertiesAbridged, RoomRadiancePropertiesAbridged, \
    ModelRadianceProperties

from .geometry import Plane, Face3D


class ShadePropertiesAbridged(BaseModel):

    type: constr(regex='^ShadePropertiesAbridged$') = 'ShadePropertiesAbridged'

    energy: ShadeEnergyPropertiesAbridged = Field(
        default=None
    )

    radiance: ShadeRadiancePropertiesAbridged = Field(
        default=None
    )


class Shade(IDdBaseModel):

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

    radiance: DoorRadiancePropertiesAbridged = Field(
        default=None
    )


class Door(IDdBaseModel):

    type: constr(regex='^Door$') = 'Door'

    geometry: Face3D = Field(
        ...,
        description='Planar Face3D for the geometry.'
    )

    boundary_condition: Union[Outdoors, Surface]

    @validator('boundary_condition')
    def surface_bc_objects(cls, v):
        if v.type == 'Surface':
            assert len(v.boundary_condition_objects) == 3, 'Door Surface boundary ' \
                'condition must have 3 boundary_condition_objects.'
        return v

    is_glass: bool = Field(
        False,
        description='Boolean to note whether this object is a glass door as opposed '
            'to an opaque door.'
    )

    indoor_shades: List[Shade] = Field(
        default=None,
        description='Shades assigned to the interior side of this object.'
    )

    outdoor_shades: List[Shade] = Field(
        default=None,
        description='Shades assigned to the exterior side of this object '
            '(eg. entryway awning).'
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

    radiance: ApertureRadiancePropertiesAbridged = Field(
        default=None
    )


class Aperture(IDdBaseModel):

    type: constr(regex='^Aperture$') = 'Aperture'

    geometry: Face3D = Field(
        ...,
        description='Planar Face3D for the geometry.'
    )

    boundary_condition: Union[Outdoors, Surface]

    @validator('boundary_condition')
    def surface_bc_objects(cls, v):
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

    radiance: FaceRadiancePropertiesAbridged = Field(
        default=None
    )


class FaceType(str, Enum):

    wall = 'Wall'
    floor = 'Floor'
    roof_ceiling = 'RoofCeiling'
    air_boundary = 'AirBoundary'


class Face(IDdBaseModel):

    type: constr(regex='^Face$') = 'Face'

    geometry: Face3D = Field(
        ...,
        description='Planar Face3D for the geometry.'
    )

    face_type: FaceType

    boundary_condition: Union[Ground, Outdoors, Adiabatic, Surface]

    @validator('boundary_condition')
    def surface_bc_objects(cls, v):
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

    @root_validator
    def check_air_boundaries_are_interior(cls, values):
        """Check that all air wall faces have a Surface boundary condition."""
        face_type, bc = values.get('face_type'), values.get('boundary_condition')
        if face_type == 'AirBoundary':
            assert bc.type == 'Surface', \
                'AirBoundaries must have "Surface" boundary conditions.'
        return values


class RoomPropertiesAbridged(BaseModel):

    type: constr(regex='^RoomPropertiesAbridged$') = 'RoomPropertiesAbridged'

    energy: RoomEnergyPropertiesAbridged = Field(
        default=None
    )

    radiance: RoomRadiancePropertiesAbridged = Field(
        default=None
    )


class Room(IDdBaseModel):

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


class Units(str, Enum):
    meters = 'Meters'
    millimeters = 'Millimeters'
    feet = 'Feet'
    inches = 'Inches'
    centimeters = 'Centimeters'


class ModelProperties(BaseModel):

    type: constr(regex='^ModelProperties$') = 'ModelProperties'

    energy: ModelEnergyProperties = Field(
        default=None
    )

    radiance: ModelRadianceProperties = Field(
        default=None
    )


class Model(IDdBaseModel):

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

    units: Units = Field(
        default=Units.meters,
        description='Text indicating the units in which the model geometry exists. '
            'This is used to scale the geometry to the correct units for simulation '
            'engines like EnergyPlus, which requires all geometry be in meters.'
    )

    tolerance: float = Field(
        default=0,
        description='The maximum difference between x, y, and z values at which '
            'vertices are considered equivalent. This value should be in the Model '
            'units and it is used in a variety of checks, including checks for '
            'whether Room faces form a closed volume and subsequently correcting all '
            'face normals point outward from the Room. A value of 0 will result '
            'in no attempt to evaluate whether Room volumes are closed or check '
            'face direction. So it is recommended that this always be a positive '
            'number when such checks have not been performed on a Model. '
            'Typical tolerances for building geometry range from 0.1 to 0.0001 '
            'depending on the units of the geometry.'
    )

    angle_tolerance: float = Field(
        default=0,
        description='The max angle difference in degrees that vertices are '
            'allowed to differ from one another in order to consider them colinear. '
            'This value is used in a variety of checks, including checks for '
            'whether Room faces form a closed volume and subsequently correcting all '
            'face normals point outward from the Room. A value of 0 will result '
            'in no attempt to evaluate whether the Room volumes is closed or check '
            'face direction. So it is recommended that this always be a positive '
            'number when such checks have not been performed on a given Model. '
            'Typical tolerances for building geometry are often around 1 degree.'
    )

    properties: ModelProperties = Field(
        ...,
        description='Extension properties for particular simulation engines '
            '(Radiance, EnergyPlus).'
    )
