"""Global modifier-set for Model."""
import pathlib
import json

from typing import List, Union
from pydantic import constr, Field

from honeybee_standards import radiance_default

from .._base import NoExtraBaseModel
from .modifierset import WallModifierSetAbridged, FloorModifierSetAbridged, \
    RoofCeilingModifierSetAbridged, ApertureModifierSetAbridged, \
    DoorModifierSetAbridged, ShadeModifierSetAbridged
from .modifier import Plastic, Glass, Glow


# import modifierset default values from honeybee standards
_DEFAULTS = json.loads(pathlib.Path(radiance_default).read_text())
_MOD_SET = [
    ms for ms in _DEFAULTS['modifier_sets']
    if ms['identifier'] == 'Generic_Interior_Visible_Modifier_Set'][0]
_MODIFIERS = [
    Plastic.parse_obj(m) if m['type'] == 'Plastic'
    else Glass.parse_obj(m) if m['type'] == 'Glass'
    else Glow.parse_obj(m) for m in _DEFAULTS['modifiers']
    ]


class GlobalModifierSet(NoExtraBaseModel):

    type: constr(regex='^GlobalModifierSet$') = 'GlobalModifierSet'

    modifiers: List[Union[Plastic, Glass, Glow]] = Field(
        default=_MODIFIERS,
        description='Global Radiance modifiers.',
        readOnly=True
    )

    wall_set: WallModifierSetAbridged = Field(
        default=WallModifierSetAbridged.parse_obj(_MOD_SET['wall_set']),
        description='Global WallModifierSet object for Model.',
        readOnly=True
    )

    floor_set: FloorModifierSetAbridged = Field(
        default=FloorModifierSetAbridged.parse_obj(_MOD_SET['floor_set']),
        description='Global FloorModifierSet object for Model.',
        readOnly=True
    )

    roof_ceiling_set: RoofCeilingModifierSetAbridged = Field(
        default=RoofCeilingModifierSetAbridged.parse_obj(_MOD_SET['roof_ceiling_set']),
        description='Global RoofCeilingModifierSet object for Model.',
        readOnly=True
    )

    aperture_set: ApertureModifierSetAbridged = Field(
        default=ApertureModifierSetAbridged.parse_obj(_MOD_SET['aperture_set']),
        description='Global ApertureModifierSet object for Model.',
        readOnly=True
    )

    door_set: DoorModifierSetAbridged = Field(
        default=DoorModifierSetAbridged.parse_obj(_MOD_SET['door_set']),
        description='Global DoorModifierSet object for Model.',
        readOnly=True
    )

    shade_set: ShadeModifierSetAbridged = Field(
        default=ShadeModifierSetAbridged.parse_obj(_MOD_SET['shade_set']),
        description='Global ShadeModifierSet object for Model.',
        readOnly=True
    )

    air_boundary_modifier: str = Field(
        default=_MOD_SET['air_boundary_modifier'],
        description='Global Modifier for AirBoundary objects in Model.',
        readOnly=True
    )
