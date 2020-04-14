"""Properties Schema"""
from pydantic import Field, constr, validator, root_validator
from typing import List, Union

from .._base import IDdBaseModel
from .modifier import Void, ModifierBase
from .modifierset import ModifierSet


class _PropertiesBaseAbridged(IDdBaseModel):
    """Base class of Abridged Radiance Properties."""

    modifier: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='A string for a Honeybee Radiance Modifier.'
        )

    modifier_blk: str = Field(
        default=None,
        min_length=1,
        max_length=100,
        description='A string for a Honeybee Radiance Modifier to be used '
                    'in direct solar simulations and in isolation studies (assessing'
                    'the contribution of individual objects).'
        )


class _PropertiesBase(IDdBaseModel):
    """Base class of Radiance Properties."""

    modifier: ModifierBase = Field(
        default=None,
        description='A Honeybee Radiance Modifier for the object.'
        )

    modifier_blk: ModifierBase = Field(
        default=None,
        description='A Honeybee Radiance Modifier to be used for this object'
                    'in direct solar simulations and in isolation studies (assessing'
                    'the contribution of individual objects).'
        )


class ApertureRadiancePropertiesAbridged(_PropertiesBase):
    """Radiance Properties for Honeybee Aperture Abridged."""

    type: constr(regex='^ApertureRadiancePropertiesAbridged$') = \
        'ApertureRadiancePropertiesAbridged'


class ApertureRadianceProperties(_PropertiesBase):
    """Radiance Properties for Honeybee Aperture."""

    type: constr(regex='^ApertureRadianceProperties$') = 'ApertureRadianceProperties'


class DoorRadiancePropertiesAbridged(_PropertiesBaseAbridged):
    """Radiance Properties for Honeybee Door Abridged."""

    type: constr(regex='^DoorRadiancePropertiesAbridged$') = \
        'DoorRadiancePropertiesAbridged'


class DoorRadianceProperties(_PropertiesBase):
    """Radiance Properties for Honeybee Door."""

    type: constr(regex='^DoorRadianceProperties$') = 'DoorRadianceProperties'


class FaceRadiancePropertiesAbridged(_PropertiesBaseAbridged):
    """Radiance Properties for Honeybee Face Abridged."""

    type: constr(regex='^FaceRadiancePropertiesAbridged$') = \
        'FaceRadiancePropertiesAbridged'


class FaceRadianceProperties(_PropertiesBase):
    """Radiance Properties for Honeybee Face."""

    type: constr(regex='^FaceRadianceProperties$') = 'FaceRadianceProperties'


class ShadeRadiancePropertiesAbridged(_PropertiesBaseAbridged):
    """Radiance Properties for Honeybee Shade Abridged."""

    type: constr(regex='^ShadeRadiancePropertiesAbridged$') = \
        'ShadeRadiancePropertiesAbridged'


class ShadeRadianceProperties(_PropertiesBase):
    """Radiance Properties for Honeybee Shade."""

    type: constr(regex='^ShadeRadianceProperties$') = 'ShadeRadianceProperties'


class ModelRadianceProperties(IDdBaseModel):
    """Radiance Properties for Honeybee Model."""

    type: constr(regex='^ModelRadianceProperties$') = 'ModelRadianceProperties'


    # TODO: Clarification: does there need to be an abridged version of all these lists?
    modifiers: List[
        ModifierBase
    ] = Field(
        default=[],
        description='A list of all unique modifiers in the model. '
                    'This includes modifiers across all Faces, Apertures, Doors, Shades, '
                    'Room ModifierSets, and the global_modifier_set. (default: []).'
        )

    blk_modifiers: List[
        ModifierBase
    ] = Field(
        default=[],
        description='A list of all unique modifier_blk assigned to Faces, Apertures '
                    'and Doors (default: []).'
        )

    room_modifiers: List[
        ModifierBase
    ] = Field(
        default=[],
        description='A list of all unique modifiers assigned to Room ModifierSets '
                    '(default: []).'
        )

    face_modifiers: List[
        ModifierBase
    ] = Field(
        default=[],
        description='A list of all unique modifiers assigned to Faces (default: []).'
        )

    shade_modifiers: List[
        ModifierBase
    ] = Field(
        default=[],
        description='A list of all unique modifiers assigned to Shades (default: []).'
        )

    bsdf_modifiers: List[
        ModifierBase
    ] = Field(
        default=[],
        description='A list of all unique BSDF modifiers in both the Model.modifiers and the '
                    'Model.blk_modifiers (default: []).'
        )

    modifier_sets: List[
        ModifierBase
    ] = Field(
        default=[],
        description='A list of all unique Room-Assigned ModifierSets in the Model '
                    '(default: []).'
        )

    #TODO: Set default as None correct, or do I need to create instance of ModifierSet
    # i.e ModifierSet(type='ModifierSet')
    global_modifier_set: ModifierSet = Field(
        default=None,
        description='A default ModifierSet object for all unassigned objects in the Model '
                    '(default: None).'
    )


# TODO: for testing will delete after PR accepted.
if __name__ == "__main__":
    print(_PropertiesBase.schema_json(indent=2))
    print(_PropertiesBaseAbridged.schema_json(indent=2))
    print(ModifierSet.schema_json(indent=2))