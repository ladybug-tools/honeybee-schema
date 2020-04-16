"""Properties Schema"""
from pydantic import Field, constr, validator, root_validator, BaseModel
from typing import List, Union

from .modifier import Plastic, Glass, BSDF, Glow, Light, Trans
from .modifierset import ModifierSet, ModifierSetAbridged

# Unioned Modifier Schema objects defined for type reference
_REFERENCE_UNION_MODIFIERS = Union[Plastic, Glass, BSDF, Glow, Light, Trans]


class _PropertiesBaseAbridged(BaseModel):
    """Base class of Abridged Radiance Properties."""

    modifier: str = Field(
        default=None,
        description='A string for a Honeybee Radiance Modifier.'
        )

    modifier_blk: str = Field(
        default=None,
        description='A string for a Honeybee Radiance Modifier to be used '
                    'in direct solar simulations and in isolation studies (assessing'
                    'the contribution of individual objects).'
        )


class ApertureRadiancePropertiesAbridged(_PropertiesBaseAbridged):
    """Radiance Properties for Honeybee Aperture Abridged."""

    type: constr(regex='^ApertureRadiancePropertiesAbridged$') = \
        'ApertureRadiancePropertiesAbridged'


class DoorRadiancePropertiesAbridged(_PropertiesBaseAbridged):
    """Radiance Properties for Honeybee Door Abridged."""

    type: constr(regex='^DoorRadiancePropertiesAbridged$') = \
        'DoorRadiancePropertiesAbridged'


class FaceRadiancePropertiesAbridged(_PropertiesBaseAbridged):
    """Radiance Properties for Honeybee Face Abridged."""

    type: constr(regex='^FaceRadiancePropertiesAbridged$') = \
        'FaceRadiancePropertiesAbridged'


class ShadeRadiancePropertiesAbridged(_PropertiesBaseAbridged):
    """Radiance Properties for Honeybee Shade Abridged."""

    type: constr(regex='^ShadeRadiancePropertiesAbridged$') = \
        'ShadeRadiancePropertiesAbridged'


class RoomRadiancePropertiesAbridged(_PropertiesBaseAbridged):
    """Abridged Radiance Properties for Honeybee Room."""

    type: constr(regex='^RoomRadiancePropertiesAbridged$') = \
        'RoomRadiancePropertiesAbridged'

    modifier_set: List[List[Union[ModifierSet, ModifierSetAbridged]]] = Field(
        default=[],
        description='A list of all unique Room-Assigned ModifierSets in the Model '
                    '(default: []).'
        )


class ModelRadianceProperties(BaseModel):
    """Radiance Properties for Honeybee Model."""

    type: constr(regex='^ModelRadianceProperties$') = 'ModelRadianceProperties'

    modifiers: List[_REFERENCE_UNION_MODIFIERS] = Field(
        default=[],
        description='A list of all unique modifiers in the model. '
                    'This includes modifiers across all Faces, Apertures, Doors, Shades, '
                    'Room ModifierSets, and the global_modifier_set. (default: []).'
        )

    blk_modifiers: List[_REFERENCE_UNION_MODIFIERS] = Field(
        default=[],
        description='A list of all unique modifier_blk assigned to Faces, Apertures '
                    'and Doors (default: []).'
        )

    modifier_sets: List[Union[ModifierSet, ModifierSetAbridged]] = Field(
        default=[],
        description='A list of all unique Room-Assigned ModifierSets in the Model '
                    '(default: []).'
        )

    global_modifier_set: str = Field(
        default=None,
        description='A string of a ModifierSet or ModifierSetAbridged object to be used as '
                    'as a default object for all unassigned objects in the Model '
                    '(default: None).'
    )


# TODO: for testing will delete after PR accepted.
if __name__ == "__main__":
    print(_PropertiesBaseAbridged.schema_json(indent=2))
    print(ModifierSet.schema_json(indent=2))