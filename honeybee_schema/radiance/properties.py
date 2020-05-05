"""Properties Schema"""
from pydantic import Field, constr
from typing import List, Union

from .modifier import _REFERENCE_UNION_MODIFIERS
from .modifierset import ModifierSet, ModifierSetAbridged
from .._base import NoExtraBaseModel


class _PropertiesBaseAbridged(NoExtraBaseModel):
    """Base class of Abridged Radiance Properties."""

    modifier: str = Field(
        default=None,
        description='A string for a Honeybee Radiance Modifier (default: None).'
        )

    modifier_blk: str = Field(
        default=None,
        description='A string for a Honeybee Radiance Modifier to be used '
                    'in direct solar simulations and in isolation studies (assessing'
                    'the contribution of individual objects) (default: None).'
        )


class ApertureRadiancePropertiesAbridged(_PropertiesBaseAbridged):
    """Radiance Properties for Honeybee Aperture Abridged."""

    try:  # see if the module has already been imported
        RadianceSubFaceStateAbridged
    except NameError:
        # import the module here (instead of at top) to avoid a circular import
        from .state import RadianceSubFaceStateAbridged

    type: constr(regex='^ApertureRadiancePropertiesAbridged$') = \
        'ApertureRadiancePropertiesAbridged'

    dynamic_group_identifier: str = Field(
        default=None,
        description="An optional string to note the dynamic group ' \
            'to which the Aperture is a part of. Apertures sharing the same ' \
            'dynamic_group_identifier will have their states change in unison. ' \
            'If None, the Aperture is assumed to be static. (default: None)."
    )

    states: List[RadianceSubFaceStateAbridged] = Field(
        default=None,
        description="An optional list of abridged states (default: None)."
    )


class DoorRadiancePropertiesAbridged(_PropertiesBaseAbridged):
    """Radiance Properties for Honeybee Door Abridged."""

    try:  # see if the module has already been imported
        RadianceSubFaceStateAbridged
    except NameError:
        # import the module here (instead of at top) to avoid a circular import
        from .state import RadianceSubFaceStateAbridged

    type: constr(regex='^DoorRadiancePropertiesAbridged$') = \
        'DoorRadiancePropertiesAbridged'

    dynamic_group_identifier: str = Field(
        default=None,
        description="An optional string to note the dynamic group ' \
            'to which the Doors is a part of. Doors sharing the same ' \
            'dynamic_group_identifier will have their states change in unison. ' \
            'If None, the Door is assumed to be static. (default: None)."
    )

    states: List[RadianceSubFaceStateAbridged] = Field(
        default=None,
        description="An optional list of abridged states (default: None)."
    )


class FaceRadiancePropertiesAbridged(_PropertiesBaseAbridged):
    """Radiance Properties for Honeybee Face Abridged."""

    type: constr(regex='^FaceRadiancePropertiesAbridged$') = \
        'FaceRadiancePropertiesAbridged'


class ShadeRadiancePropertiesAbridged(_PropertiesBaseAbridged):
    """Radiance Properties for Honeybee Shade Abridged."""

    try:  # see if the module has already been imported
        RadianceShadeStateAbridged
    except NameError:
        # import the module here (instead of at top) to avoid a circular import
        from .state import RadianceShadeStateAbridged

    type: constr(regex='^ShadeRadiancePropertiesAbridged$') = \
        'ShadeRadiancePropertiesAbridged'

    dynamic_group_identifier: str = Field(
        default=None,
        description="An optional string to note the dynamic group ' \
            'to which the Shade is a part of. Shades sharing the same ' \
            'dynamic_group_identifier will have their states change in unison. ' \
            'If None, the Shade is assumed to be static. (default: None)."
    )

    states: List[RadianceShadeStateAbridged] = Field(
        default=None,
        description="An optional list of abridged states (default: None)."
    )


class RoomRadiancePropertiesAbridged(NoExtraBaseModel):
    """Abridged Radiance Properties for Honeybee Room."""

    type: constr(regex='^RoomRadiancePropertiesAbridged$') = \
        'RoomRadiancePropertiesAbridged'

    modifier_set: str = Field(
        default=None,
        description='An identifier for a unique Room-Assigned ModifierSet '
                    '(default: None).'
        )


class ModelRadianceProperties(NoExtraBaseModel):
    """Radiance Properties for Honeybee Model."""

    type: constr(regex='^ModelRadianceProperties$') = 'ModelRadianceProperties'

    modifiers: List[_REFERENCE_UNION_MODIFIERS] = Field(
        default=[],
        description='A list of all unique modifiers in the model. '
                    'This includes modifiers across all Faces, Apertures, Doors, '
                    'Shades, Room ModifierSets, and the global_modifier_set '
                    '(default: []).'
        )

    modifier_sets: List[Union[ModifierSet, ModifierSetAbridged]] = Field(
        default=[],
        description='A list of all unique Room-Assigned ModifierSets in the Model '
                    '(default: []).'
        )

    global_modifier_set: str = Field(
        default=None,
        description='Identifier of a ModifierSet or ModifierSetAbridged object to be '
                    'used as as a default object for all unassigned objects in the '
                    'Model (default: None).'
        )
