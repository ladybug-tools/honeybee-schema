"""Model schema and the 5 geometry objects that define it."""
from typing import List, Union, Literal
from enum import Enum
from pydantic import BaseModel, Field, field_validator, model_validator

from ._base import IDdBaseModel
from .boundarycondition import Outdoors, Surface, Ground, Adiabatic, OtherSideTemperature

from .energy.properties import ShadeEnergyPropertiesAbridged, \
    DoorEnergyPropertiesAbridged, ApertureEnergyPropertiesAbridged, \
    FaceEnergyPropertiesAbridged, RoomEnergyPropertiesAbridged, \
    ModelEnergyProperties, ShadeMeshEnergyPropertiesAbridged

from .radiance.properties import ShadeRadiancePropertiesAbridged, \
    DoorRadiancePropertiesAbridged, ApertureRadiancePropertiesAbridged, \
    FaceRadiancePropertiesAbridged, RoomRadiancePropertiesAbridged, \
    ModelRadianceProperties, ShadeMeshRadiancePropertiesAbridged

from .doe2.properties import RoomDoe2Properties, ModelDoe2Properties

from .geometry import Face3D, Mesh3D


class ShadeMeshPropertiesAbridged(BaseModel):

    type: Literal['ShadeMeshPropertiesAbridged'] = 'ShadeMeshPropertiesAbridged'

    energy: Union[ShadeMeshEnergyPropertiesAbridged, None] = Field(
        default=None
    )

    radiance: Union[ShadeMeshRadiancePropertiesAbridged, None] = Field(
        default=None
    )


class ShadeMesh(IDdBaseModel):

    type: Literal['ShadeMesh'] = 'ShadeMesh'

    geometry: Mesh3D = Field(
        ...,
        description='A Mesh3D for the geometry.'
    )

    properties: ShadeMeshPropertiesAbridged = Field(
        ...,
        description='Extension properties for particular simulation engines '
        '(Radiance, EnergyPlus).'
    )

    is_detached: bool = Field(
        True,
        description='Boolean to note whether this shade is detached from any of '
        'the other geometry in the model. Cases where this should be True include '
        'shade representing surrounding buildings or context.'
    )


class ShadePropertiesAbridged(BaseModel):

    type: Literal['ShadePropertiesAbridged'] = 'ShadePropertiesAbridged'

    energy: Union[ShadeEnergyPropertiesAbridged, None] = Field(
        default=None
    )

    radiance: Union[ShadeRadiancePropertiesAbridged, None] = Field(
        default=None
    )


class Shade(IDdBaseModel):

    type: Literal['Shade'] = 'Shade'

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

    type: Literal['DoorPropertiesAbridged'] = 'DoorPropertiesAbridged'

    energy: Union[DoorEnergyPropertiesAbridged, None] = Field(
        default=None
    )

    radiance: Union[DoorRadiancePropertiesAbridged, None] = Field(
        default=None
    )


class Door(IDdBaseModel):

    type: Literal['Door'] = 'Door'

    geometry: Face3D = Field(
        ...,
        description='Planar Face3D for the geometry.'
    )

    boundary_condition: Union[Outdoors, Surface]

    @field_validator('boundary_condition')
    @classmethod
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

    indoor_shades: Union[List[Shade], None] = Field(
        default=None,
        description='Shades assigned to the interior side of this object.'
    )

    outdoor_shades: Union[List[Shade], None] = Field(
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

    type: Literal['AperturePropertiesAbridged'] = 'AperturePropertiesAbridged'

    energy: Union[ApertureEnergyPropertiesAbridged, None] = Field(
        default=None
    )

    radiance: Union[ApertureRadiancePropertiesAbridged, None] = Field(
        default=None
    )


class Aperture(IDdBaseModel):

    type: Literal['Aperture'] = 'Aperture'

    geometry: Face3D = Field(
        ...,
        description='Planar Face3D for the geometry.'
    )

    boundary_condition: Union[Outdoors, Surface]

    @field_validator('boundary_condition')
    @classmethod
    def surface_bc_objects(cls, v):
        if v.type == 'Surface':
            assert len(v.boundary_condition_objects) == 3, 'Aperture Surface boundary ' \
                'condition must have 3 boundary_condition_objects.'
        return v

    is_operable: bool = Field(
        False,
        description='Boolean to note whether the Aperture can be opened for ventilation.'
    )

    indoor_shades: Union[List[Shade], None] = Field(
        default=None,
        description='Shades assigned to the interior side of this object '
        '(eg. window sill, light shelf).'
    )

    outdoor_shades: Union[List[Shade], None] = Field(
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

    type: Literal['FacePropertiesAbridged'] = 'FacePropertiesAbridged'

    energy: Union[FaceEnergyPropertiesAbridged, None] = Field(
        default=None
    )

    radiance: Union[FaceRadiancePropertiesAbridged, None] = Field(
        default=None
    )


class FaceType(str, Enum):

    wall = 'Wall'
    floor = 'Floor'
    roof_ceiling = 'RoofCeiling'
    air_boundary = 'AirBoundary'


class Face(IDdBaseModel):

    type: Literal['Face'] = 'Face'

    geometry: Face3D = Field(
        ...,
        description='Planar Face3D for the geometry.'
    )

    face_type: FaceType

    boundary_condition: Union[Ground, Outdoors, Adiabatic, Surface, OtherSideTemperature]

    @field_validator('boundary_condition')
    @classmethod
    def surface_bc_objects(cls, v):
        if v.type == 'Surface':
            assert len(v.boundary_condition_objects) == 2, 'Face Surface boundary ' \
                'condition must have 2 boundary_condition_objects.'
        return v

    apertures: Union[List[Aperture], None] = Field(
        default=None,
        description='Apertures assigned to this Face. Should be coplanar with this '
        'Face and completely within the boundary of the Face to be valid.'
    )

    doors: Union[List[Door], None] = Field(
        default=None,
        description='Doors assigned to this Face. Should be coplanar with this '
        'Face and completely within the boundary of the Face to be valid.'
    )

    indoor_shades: Union[List[Shade], None] = Field(
        default=None,
        description='Shades assigned to the interior side of this object.'
    )

    outdoor_shades: Union[List[Shade], None] = Field(
        default=None,
        description='Shades assigned to the exterior side of this object '
        '(eg. balcony, overhang).'
    )

    properties: FacePropertiesAbridged = Field(
        ...,
        description='Extension properties for particular simulation engines '
        '(Radiance, EnergyPlus).'
    )

    @model_validator(mode='after')
    def check_air_boundaries_are_interior(self):
        """Check that all air wall faces have a Surface boundary condition."""
        if self.face_type == 'AirBoundary':
            if self.boundary_condition.type != 'Surface':
                raise ValueError(
                    'AirBoundaries must have "Surface" boundary conditions.'
                )
        return self


class RoomPropertiesAbridged(BaseModel):

    type: Literal['RoomPropertiesAbridged'] = 'RoomPropertiesAbridged'

    energy: Union[RoomEnergyPropertiesAbridged, None] = Field(
        default=None
    )

    radiance: Union[RoomRadiancePropertiesAbridged, None] = Field(
        default=None
    )

    doe2: Union[RoomDoe2Properties, None] = Field(
        default=None
    )


class Room(IDdBaseModel):

    type: Literal['Room'] = 'Room'

    faces: List[Face] = Field(
        ...,
        min_length=4,
        description='Faces that together form the closed volume of a room.'
    )

    indoor_shades: Union[List[Shade], None] = Field(
        default=None,
        description='Shades assigned to the interior side of this object '
        '(eg. partitions, tables).'
    )

    outdoor_shades: Union[List[Shade], None] = Field(
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

    zone: Union[str, None] = Field(
        default=None,
        description='Text string for for the zone identifier to which this Room belongs. '
        'Rooms sharing the same zone identifier are considered part of the same zone '
        'in a Model. If the zone identifier has not been specified, it will be '
        'the same as the Room identifier in the destination engine. Note that this '
        'property has no character restrictions.'
    )

    story: Union[str, None] = Field(
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

    type: Literal['ModelProperties'] = 'ModelProperties'

    energy: Union[ModelEnergyProperties, None] = Field(
        default=None
    )

    radiance: Union[ModelRadianceProperties, None] = Field(
        default=None
    )

    doe2: Union[ModelDoe2Properties, None] = Field(
        default=None
    )


class Model(IDdBaseModel):

    type: Literal['Model'] = 'Model'

    version: str = Field(
        default='0.0.0',
        pattern=r'^([0-9]+)\.([0-9]+)\.([0-9]+)$',
        description='Text string for the current version of the schema.'
    )

    rooms: Union[List[Room], None] = Field(
        default=None,
        description='A list of Rooms in the model.'
    )

    orphaned_faces: Union[List[Face], None] = Field(
        default=None,
        description='A list of Faces in the model that lack a parent Room. Note that '
        'orphaned Faces are not acceptable for Models that are to be exported '
        'for energy simulation.'
    )

    orphaned_shades: Union[List[Shade], None] = Field(
        default=None,
        description='A list of Shades in the model that lack a parent.'
    )

    orphaned_apertures: Union[List[Aperture], None] = Field(
        default=None,
        description='A list of Apertures in the model that lack a parent Face. '
        'Note that orphaned Apertures are not acceptable for Models that are '
        'to be exported for energy simulation.'
    )

    orphaned_doors: Union[List[Door], None] = Field(
        default=None,
        description='A list of Doors in the model that lack a parent Face. '
        'Note that orphaned Doors are not acceptable for Models that are '
        'to be exported for energy simulation.'
    )

    shade_meshes: Union[List[ShadeMesh], None] = Field(
        default=None,
        description='A list of ShadeMesh in the model.'
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
