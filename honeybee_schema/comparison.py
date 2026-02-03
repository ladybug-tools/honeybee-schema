"""Schema for the comparison object returned by the comparison command"""
from typing import List, Literal, Union
from enum import Enum
from pydantic import BaseModel, Field


class GeometryObjectTypes(str, Enum):
    """Types of Honeybee geometry objects."""
    shade = 'Shade'
    aperture = 'Aperture'
    door = 'Door'
    face = 'Face'
    room = 'Room'


class _DiffObjectBase(BaseModel):

    element_type: GeometryObjectTypes = Field(
        ...,
        description='Text for the type of object that has been changed.'
    )

    element_id: str = Field(
        ...,
        pattern=r'^[^,;!\n\t]+$',
        min_length=1,
        max_length=100,
        description='Text string for the unique object ID that has changed.'
    )

    element_name: Union[str, None] = Field(
        None,
        description='Text string for the display name of the object that has changed.'
    )


class ChangedObject(_DiffObjectBase):

    type: Literal['ChangedObject'] = 'ChangedObject'

    geometry_changed: bool = Field(
        ...,
        description='A boolean to note whether the geometry of the object has changed '
        '(True) or not (False). For the case of a Room, any change in the geometry of '
        'child Faces, Apertures or Doors will cause this property to be True. Note that '
        'this property is only True if the change in geometry produces a visible '
        'change greater than the base model tolerance. So converting the model '
        'between different unit systems, removing colinear vertices, or doing '
        'other transformations that are common for export to simulation engines '
        'will not trigger this property to become True.'
    )

    energy_changed: bool = Field(
        False,
        description='A boolean to note whether the energy properties of the object '
        'have changed (True) or not (False) such that it is possible for the '
        'properties of the changed object to be applied to the base model. '
        'For Rooms, this property will only be true if the energy property '
        'assigned to the Room has changed and will not be true if a property '
        'assigned to an individual child Face or Aperture has changed.'
    )

    radiance_changed: bool = Field(
        False,
        description='A boolean to note whether the radiance properties of the object '
        'have changed (True) or not (False) such that it is possible for the '
        'properties of the changed object to be applied to the base model. '
        'For Rooms, this property will only be true if the radiance property '
        'assigned to the Room has changed and will not be true if a property '
        'assigned to an individual child Face or Aperture has changed.'
    )

    geometry: List[dict] = Field(
        ...,
        description='A list of DisplayFace3D dictionaries for the new, changed '
        'geometry. The schema of DisplayFace3D can be found in the ladybug-display-'
        'schema documentation (https://www.ladybug.tools/ladybug-display-schema) '
        'and these objects can be used to generate visualizations of individual '
        'objects that have been changed. Note that this attribute is always '
        'included in the ChangedObject, even when geometry_changed is False.'
    )

    existing_geometry: Union[List[dict], None] = Field(
        default=None,
        description='A list of DisplayFace3D dictionaries for the existing (base) '
        'geometry. The schema of DisplayFace3D can be found in the ladybug-display-'
        'schema documentation (https://www.ladybug.tools/ladybug-display-schema) '
        'and these objects can be used to generate visualizations of individual '
        'objects that have been changed. This attribute is optional and will '
        'NOT be output if geometry_changed is False.'
    )


class DeletedObject(_DiffObjectBase):

    type: Literal['DeletedObject'] = 'DeletedObject'

    geometry: List[dict] = Field(
        ...,
        description='A list of DisplayFace3D dictionaries for the deleted '
        'geometry. The schema of DisplayFace3D can be found in the ladybug-display-'
        'schema documentation (https://www.ladybug.tools/ladybug-display-schema) '
        'and these objects can be used to generate visualizations of individual '
        'objects that have been deleted.'
    )


class AddedObject(_DiffObjectBase):

    type: Literal['AddedObject'] = 'AddedObject'

    geometry: List[dict] = Field(
        ...,
        description='A list of DisplayFace3D dictionaries for the added '
        'geometry. The schema of DisplayFace3D can be found in the ladybug-display-'
        'schema documentation (https://www.ladybug.tools/ladybug-display-schema) '
        'and these objects can be used to generate visualizations of individual '
        'objects that have been added.'
    )


class ComparisonReport(BaseModel):

    type: Literal['ComparisonReport'] = 'ComparisonReport'

    changed_objects: Union[List[ChangedObject], None] = Field(
        default=None,
        description='A list of ChangedObject definitions for each top-level object '
        'that has changed in the model. To be a changed object, the object identifier '
        'must be the same in both models but some other property (either geometry '
        'or extension attributes) has experienced a meaningful change.'
    )

    deleted_objects: Union[List[DeletedObject], None] = Field(
        default=None,
        description='A list of DeletedObject definitions for each top-level object '
        'that has been deleted in the process of going from the base model to the '
        'new model.'
    )

    added_objects: Union[List[AddedObject], None] = Field(
        default=None,
        description='A list of AddedObject definitions for each top-level object '
        'that has been added in the process of going from the base model to the '
        'new model.'
    )


class ChangedInstruction(_DiffObjectBase):

    type: Literal['ChangedInstruction'] = 'ChangedInstruction'

    update_geometry: bool = Field(
        True,
        description='A boolean to note whether the geometry of the object in the '
        'new/updated model should replace the base/existing geometry (True) or '
        'the existing geometry should be kept (False).'
    )

    update_energy: bool = Field(
        True,
        description='A boolean to note whether the energy properties of the '
        'object in the new/updated model should replace the base/existing energy '
        'properties (True) or the base/existing energy properties should '
        'be kept (False).'
    )

    update_radiance: bool = Field(
        True,
        description='A boolean to note whether the radiance properties of the '
        'object in the new/updated model should replace the base/existing radiance '
        'properties (True) or the base/existing radiance properties should '
        'be kept (False).'
    )


class DeletedInstruction(_DiffObjectBase):

    type: Literal['DeletedInstruction'] = 'DeletedInstruction'


class AddedInstruction(_DiffObjectBase):

    type: Literal['AddedInstruction'] = 'AddedInstruction'


class SyncInstructions(BaseModel):

    type: Literal['SyncInstructions'] = 'SyncInstructions'

    changed_objects: Union[List[ChangedInstruction], None] = Field(
        default=None,
        description='A list of ChangedInstruction definitions for each top-level '
        'object with properties to transfer from the new/updated model to the '
        'base/existing model.'
    )

    deleted_objects: Union[List[DeletedInstruction], None] = Field(
        default=None,
        description='A list of DeletedInstruction definitions for each top-level object '
        'to be deleted from the base/existing model.'
    )

    added_objects: Union[List[AddedInstruction], None] = Field(
        default=None,
        description='A list of AddedInstruction definitions for each top-level object '
        'to be added to the base/existing model from the new/updated model.'
    )
