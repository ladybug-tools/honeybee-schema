"""Schema for the error objects returned by the validation command"""
from pydantic import BaseModel, Field, constr
from typing import List, Union
from enum import Enum

from .geometry import Point3D, LineSegment3D


class ExtensionTypes(str, Enum):
    """Types of Honeybee/Dragonfly extensions."""
    core = 'Core'
    radiance = 'Radiance'
    energy = 'Energy'


class ObjectTypes(str, Enum):
    """Types of Honeybee objects."""
    shade = 'Shade'
    aperture = 'Aperture'
    door = 'Door'
    sub_face = 'SubFace'
    face = 'Face'
    room = 'Room'
    sensor_grid = 'SensorGrid'
    view = 'View'
    modifier = 'Modifier'
    modifier_set = 'ModifierSet'
    material = 'Material'
    construction = 'Construction'
    construction_set = 'ConstructionSet'
    schedule_type_limit = 'ScheduleTypeLimit'
    schedule = 'Schedule'
    program_type = 'ProgramType'
    hvac = 'HVAC'
    shw = 'SHW'
    roof_spec = 'RoofSpecification'
    room_2d = 'Room2D'
    story = 'Story'
    building = 'Building'


class ParentTypes(str, Enum):
    """Types of Honeybee objects that can be parents."""
    aperture = 'Aperture'
    door = 'Door'
    face = 'Face'
    room = 'Room'
    story = 'Story'
    building = 'Building'


class ValidationParent(BaseModel):

    type: constr(regex='^ValidationParent$') = 'ValidationParent'

    parent_type: ParentTypes = Field(
        ...,
        description='Text for the type of object that the parent is.'
    )

    id: str = Field(
        ...,
        regex=r'^[.A-Za-z0-9_-]+$',
        min_length=1,
        max_length=100,
        description='Text string for the unique ID of the parent object.'
    )

    name: str = Field(
        default=None,
        description='Display name of the parent object.'
    )


class ValidationError(BaseModel):

    type: constr(regex='^ValidationError$') = 'ValidationError'

    code: str = Field(
        ...,
        min_length=6,
        max_length=6,
        regex=r'([0-9]+)',
        description='Text with 6 digits for the error code. The first two digits '
        'indicate whether the error is a core honeybee error (00) vs. an extension '
        'error (any non-zero number). The second two digits indicate the nature '
        'of the error (00 is an identifier error, 01 is a geometry error, 02 is an '
        'adjacency error). The third two digits are used to give a unique ID to '
        'each condition moving upwards from more specific/detailed objects/errors '
        'to coarser/more abstract objects/errors. A full list of error codes can '
        'be found here: https://docs.pollination.cloud/user-manual/get-started/'
        'troubleshooting/help-with-modeling-error-codes'
    )

    error_type: str = Field(
        ...,
        description='A human-readable version of the error code, typically not more '
        'than five words long.'
    )

    extension_type: ExtensionTypes = Field(
        ...,
        description='Text for the Honeybee extension from which the error originated '
        '(from the ExtensionTypes enumeration).'
    )

    element_type: ObjectTypes = Field(
        ...,
        description='Text for the type of object that caused the error.'
    )

    element_id: List[
        constr(min_length=1, max_length=100, regex=r'^[^,;!\n\t]+$')
    ] = Field(
        ...,
        description='A list of text strings for the unique object IDs that caused '
        'the error. The list typically contains a single item but there are some types '
        'errors that stem from multiple objects like mis-matched area adjacencies '
        'or overlapping Room geometries. Note that the IDs in this list can be the '
        'identifier of a core object like a Room or a Face or it can be for an '
        'extension object like a SensorGrid or a Construction.'
    )

    element_name: List[str] = Field(
        default=None,
        description='A list of text strings for the display names of the objects '
        'that caused the error.'
    )

    message: str = Field(
        ...,
        description='Text for the error message with a detailed description of '
        'what exactly is invalid about the element.'
    )

    parents: List[List[ValidationParent]] = Field(
        default=None,
        description='A list lists where each sub-list corresponds to one of the '
        'objects in the element_id property. Each sub-list contains information for '
        'the parent objects of the object that caused the error. '
        'This can be useful for locating the problematic object in the model. '
        'This will contain 1 item for a Face with a parent Room. It will contain 2 '
        'for an Aperture that has a parent Face with a parent Room.'
    )

    top_parents: List[ValidationParent] = Field(
        default=None,
        description='A list of top-level parent objects for the specific case of '
        'duplicate child-object identifiers, where several top-level parents '
        'are involved.'
    )

    helper_geometry: List[Union[Point3D, LineSegment3D]] = Field(
        default=None,
        description='An optional list of geometry objects that helps illustrate '
        'where exactly issues with invalid geometry exist within the Honeybee object. '
        'Examples include the naked and non-manifold line segments for non-solid Room '
        'geometries, the points of self-intersection for cases of self-intersecting '
        'geometry and out-of-plane vertices for non-planar objects. Oftentimes, '
        'zooming directly to these helper geometries will help end users understand '
        'invalid situations in their model faster than simple zooming to the invalid '
        'Honeybee object in its totality.'
    )


class ValidationReport(BaseModel):

    type: constr(regex='^ValidationReport$') = 'ValidationReport'

    app_name: str = Field(
        'Honeybee',
        description='Text string for the name of the application that performed '
        'the validation. This is typically either Honeybee or Dragonfly.'
    )

    app_version: str = Field(
        ...,
        regex=r'([0-9]+)\.([0-9]+)\.([0-9]+)',
        description='Text string for the version of honeybee-core or dragonfly-core '
        'that performed the validation.'
    )

    schema_version: str = Field(
        ...,
        regex=r'([0-9]+)\.([0-9]+)\.([0-9]+)',
        description='Text string for the version of honeybee-schema or dragonfly-schema '
        'that performed the validation.'
    )

    valid: bool = Field(
        ...,
        description='Boolean to note whether the Model is valid or not.'
    )

    fatal_error: str = Field(
        '',
        description='A text string containing an exception if the Model failed to '
        'serialize. It will be an empty string if serialization was successful.'
    )

    errors: List[ValidationError] = Field(
        default=None,
        description='A list of objects for each error that was discovered in the model. '
        'This will be an empty list or None if no errors were found.'
    )
