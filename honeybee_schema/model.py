"""Model schema and the 5 geometry objects that define it."""
from pydantic import BaseModel, Field, validator, root_validator, constr
from typing import List, Union
from enum import Enum

from ._base import IDdBaseModel
from .boundarycondition import Outdoors, Surface, Ground, Adiabatic, OtherSideTemperature

from .energy.properties import ShadeEnergyPropertiesAbridged, \
    DoorEnergyPropertiesAbridged, ApertureEnergyPropertiesAbridged, \
    FaceEnergyPropertiesAbridged, RoomEnergyPropertiesAbridged, \
    ModelEnergyProperties

from .radiance.properties import ShadeRadiancePropertiesAbridged, \
    DoorRadiancePropertiesAbridged, ApertureRadiancePropertiesAbridged, \
    FaceRadiancePropertiesAbridged, RoomRadiancePropertiesAbridged, \
    ModelRadianceProperties

from .geometry import Face3D


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

    is_detached: bool = Field(
        False,
        description='Boolean to note whether this shade is detached from any of '
        'the other geometry in the model. Cases where this should be True include '
        'shade representing surrounding buildings or context. Note that this '
        'should always be False for shades assigned to parent objects.'
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

    boundary_condition: Union[Ground, Outdoors, Adiabatic, Surface, OtherSideTemperature]

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

    multiplier: int = Field(
        1,
        ge=1,
        description='An integer noting how many times this Room is repeated. '
        'Multipliers are used to speed up the calculation when similar Rooms are '
        'repeated more than once. Essentially, a given simulation with the '
        'Room is run once and then the result is multiplied by the multiplier.'
    )

    exclude_floor_area: bool = Field(
        False,
        description='A boolean for whether the Room floor area contributes to Models '
        'it is a part of. Note that this will not affect the floor_area property of '
        'this Room itself but it will ensure the Room floor area is excluded from '
        'any calculations when the Room is part of a Model, including EUI calculations.'
    )

    story: str = Field(
        default=None,
        description='Text string for the story identifier to which this Room belongs. '
        'Rooms sharing the same story identifier are considered part of the same '
        'story in a Model. Note that this property has no character restrictions.'
    )

    properties: RoomPropertiesAbridged = Field(
        ...,
        description='Extension properties for particular simulation engines '
        '(Radiance, EnergyPlus).'
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

    version: str = Field(
        default='0.0.0',
        regex=r'([0-9]+)\.([0-9]+)\.([0-9]+)',
        description='Text string for the current version of the schema.'
    )

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
        default=0.01,
        ge=0,
        description='The maximum difference between x, y, and z values at which '
        'vertices are considered equivalent. This value should be in the Model '
        'units and it is used in a variety of checks, including checks for '
        'whether Room faces form a closed volume and subsequently correcting all '
        'face normals point outward from the Room. A value of 0 will result '
        'in bypassing all checks so it is recommended that this always be a positive '
        'number when such checks have not already been performed on a Model. '
        'The default of 0.01 is suitable for models in meters.'
    )

    angle_tolerance: float = Field(
        default=1.0,
        ge=0,
        description='The max angle difference in degrees that vertices are '
        'allowed to differ from one another in order to consider them colinear. '
        'This value is used in a variety of checks, including checks for '
        'whether Room faces form a closed volume and subsequently correcting all '
        'face normals point outward from the Room. A value of 0 will result '
        'in bypassing all checks so it is recommended that this always be a positive '
        'number when such checks have not already been performed on a given Model.'
    )

    properties: ModelProperties = Field(
        ...,
        description='Extension properties for particular simulation engines '
        '(Radiance, EnergyPlus).'
    )
