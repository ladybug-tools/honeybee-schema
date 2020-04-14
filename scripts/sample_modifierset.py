# coding=utf-8
from __future__ import division

from honeybee_radiance.modifierset import ModifierSet
from honeybee_radiance.lib.modifiersets import generic_modifier_set_visible
import honeybee_radiance.lib.modifiers as modifiers

import os
import json


def modifierset_abridged_complete(directory):
    dest_file = os.path.join(directory, 'modifierset_abridged_complete.json')
    with open(dest_file, 'w') as fp:
        json.dump(generic_modifier_set_visible.to_dict(True, False), fp, indent=4)


def modifierset_abridged_partial_exterior(directory):
    mod_set = ModifierSet('Generic_Exterior_Visible_Modifier_Set')
    mod_set.wall_set.exterior_modifier = modifiers.generic_wall_exterior
    mod_set.floor_set.exterior_modifier = modifiers.generic_floor_exterior
    mod_set.roof_ceiling_set.exterior_modifier = modifiers.generic_roof_exterior
    dest_file = os.path.join(directory, 'modifierset_abridged_partial_exterior.json')
    with open(dest_file, 'w') as fp:
        json.dump(mod_set.to_dict(True, True), fp, indent=4)


def modifierset_complete(directory):
    dest_file = os.path.join(directory, 'modifierset_complete.json')
    with open(dest_file, 'w') as fp:
        json.dump(generic_modifier_set_visible.to_dict(False, False), fp, indent=4)


def modifierset_partial_exterior(directory):
    mod_set = ModifierSet('Generic_Exterior_Visible_Modifier_Set')
    mod_set.wall_set.exterior_modifier = modifiers.generic_wall_exterior
    mod_set.floor_set.exterior_modifier = modifiers.generic_floor_exterior
    mod_set.roof_ceiling_set.exterior_modifier = modifiers.generic_roof_exterior
    dest_file = os.path.join(directory, 'modifierset_partial_exterior.json')
    with open(dest_file, 'w') as fp:
        json.dump(mod_set.to_dict(False, True), fp, indent=4)


# run all functions within the file
master_dir = os.path.split(os.path.dirname(__file__))[0]
sample_directory = os.path.join(master_dir, 'samples', 'modifier_set')

modifierset_abridged_complete(sample_directory)
modifierset_abridged_partial_exterior(sample_directory)
modifierset_complete(sample_directory)
modifierset_partial_exterior(sample_directory)
