"""Schema for the error objects returned by the validation command"""
from pydantic import BaseModel, Field, constr
from typing import List
from enum import Enum


class ExtensionTypes(str, Enum):
    """Types of Honeybee extensions."""
    core = 'Core'
    radiance = 'Radiance'
    energy = 'Energy'


class ObjectTypes(str, Enum):
    """Types of Honeybee objects."""
    shade = 'Shade'
    aperture = 'Aperture'
    door = 'Door'
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


class ParentTypes(str, Enum):
    """Types of Honeybee objects that can be parents."""
    aperture = 'Aperture'
    door = 'Door'
    face = 'Face'
    room = 'Room'


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

    element_id: str = Field(
        ...,
        regex=r'^[^,;!\n\t]+$',
        min_length=1,
        max_length=100,
        description='Text string for the unique object ID that caused the error. '
        'Note that this can be the identifier of a core object like a Room or a Face. '
        'Or it can be for an extension object like a SensorGrid or a Construction.'
    )

    element_name: str = Field(
        default=None,
        description='Display name of the object that caused the error.'
    )

    message: str = Field(
        ...,
        description='Text for the error message with a detailed description of '
        'what exactly is invalid about the element.'
    )

    parents: List[ValidationParent] = Field(
        default=None,
        description='A list of the parent objects for the object that caused the error. '
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


class ValidationReport(BaseModel):

    type: constr(regex='^ValidationReport$') = 'ValidationReport'

    honeybee_core: str = Field(
        ...,
        regex=r'([0-9]+)\.([0-9]+)\.([0-9]+)',
        description='Text string for the version of honeybee-core that '
        'performed the validation.'
    )

    honeybee_schema: str = Field(
        ...,
        regex=r'([0-9]+)\.([0-9]+)\.([0-9]+)',
        description='Text string for the version of honeybee-schema that '
        'performed the validation.'
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
