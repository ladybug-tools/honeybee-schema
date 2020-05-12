# coding=utf-8
from __future__ import division

from honeybee_radiance.primitive import VOID
from honeybee_radiance.modifier.material import Metal, Trans, Light, Mirror, BSDF

from honeybee_radiance.lib.modifiers import generic_wall, generic_ceiling, \
    black, generic_exterior_window, air_boundary, white_glow

import os
import json


def modifier_plastic_generic_wall(directory):
    dest_file = os.path.join(directory, 'modifier_plastic_generic_wall.json')
    with open(dest_file, 'w') as fp:
        json.dump(generic_wall.to_dict(), fp, indent=4)


def modifier_plastic_generic_ceiling(directory):
    dest_file = os.path.join(directory, 'modifier_plastic_generic_ceiling.json')
    with open(dest_file, 'w') as fp:
        json.dump(generic_ceiling.to_dict(), fp, indent=4)


def modifier_plastic_black(directory):
    dest_file = os.path.join(directory, 'modifier_plastic_black.json')
    with open(dest_file, 'w') as fp:
        json.dump(black.to_dict(), fp, indent=4)


def modifier_metal(directory):
    metal = Metal.from_single_reflectance('sheet_metal_0.5', 0.5, 0.95)
    dest_file = os.path.join(directory, 'modifier_metal.json')
    with open(dest_file, 'w') as fp:
        json.dump(metal.to_dict(), fp, indent=4)


def modifier_glass_generic_exterior_window(directory):
    dest_file = os.path.join(directory, 'modifier_glass_generic_exterior_window.json')
    with open(dest_file, 'w') as fp:
        json.dump(generic_exterior_window.to_dict(), fp, indent=4)


def modifier_glass_air_boundary(directory):
    dest_file = os.path.join(directory, 'modifier_glass_air_boundary.json')
    with open(dest_file, 'w') as fp:
        json.dump(air_boundary.to_dict(), fp, indent=4)


def modifier_trans_tree_foliage(directory):
    tree_leaves = Trans.from_single_reflectance('Foliage_0.3', 0.3, 0.0, 0.1, 0.15, 0.15)
    dest_file = os.path.join(directory, 'modifier_trans_tree_foliage.json')
    with open(dest_file, 'w') as fp:
        json.dump(tree_leaves.to_dict(), fp, indent=4)


def modifier_glow_white(directory):
    dest_file = os.path.join(directory, 'modifier_glow_white.json')
    with open(dest_file, 'w') as fp:
        json.dump(white_glow.to_dict(), fp, indent=4)


def modifier_light_green_spotlight(directory):
    green_spot = Light('Green_Spotlight', 0, 1, 0)
    dest_file = os.path.join(directory, 'modifier_light_green_spotlight.json')
    with open(dest_file, 'w') as fp:
        json.dump(green_spot.to_dict(), fp, indent=4)


def modifier_mirror_typical(directory):
    mirror_typical = Mirror('Silver_Glass_Typical_Mirror', 0.85, 0.85, 0.85)
    dest_file = os.path.join(directory, 'modifier_mirror_typical.json')
    with open(dest_file, 'w') as fp:
        json.dump(mirror_typical.to_dict(), fp, indent=4)


def modifier_mirror_invisible(directory):
    mirror_invisible = Mirror('Invisible_Mirror', 1.0, 1.0, 1.0, alternate_material=VOID)
    dest_file = os.path.join(directory, 'modifier_mirror_invisible.json')
    with open(dest_file, 'w') as fp:
        json.dump(mirror_invisible.to_dict(), fp, indent=4)


def modifier_bsdf_klemsfull(directory):
    relative_path = './scripts/bsdf/klemsfull.xml'
    klemsfull = BSDF(relative_path)
    dest_file = os.path.join(directory, 'modifier_bsdf_klemsfull.json')
    json.dumps(klemsfull.to_dict(), indent=4)
    with open(dest_file, 'w') as fp:
        json.dump(klemsfull.to_dict(), fp, indent=4)


# run all functions within the file
master_dir = os.path.split(os.path.dirname(__file__))[0]
sample_directory = os.path.join(master_dir, 'samples', 'modifier')

modifier_plastic_generic_wall(sample_directory)
modifier_plastic_generic_ceiling(sample_directory)
modifier_plastic_black(sample_directory)
modifier_metal(sample_directory)
modifier_glass_generic_exterior_window(sample_directory)
modifier_glass_air_boundary(sample_directory)
modifier_trans_tree_foliage(sample_directory)
modifier_glow_white(sample_directory)
modifier_light_green_spotlight(sample_directory)
modifier_mirror_typical(sample_directory)
modifier_mirror_invisible(sample_directory)
modifier_bsdf_klemsfull(sample_directory)
