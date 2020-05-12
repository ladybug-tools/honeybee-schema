from honeybee_schema.radiance.modifier import Plastic, Glass, BSDF, Glow, Light, \
    Trans, Mirror, Metal
from copy import copy
from pydantic import ValidationError
import pytest
import os
import json

# target folder where all of the samples live
root = os.path.dirname(os.path.dirname(__file__))
target_folder = os.path.join(root, 'samples', 'modifier')


def test_modifier_plastic_black():
    file_path = os.path.join(target_folder, 'modifier_plastic_black.json')
    Plastic.parse_file(file_path)


def test_modifier_plastic_generic_ceiling():
    file_path = os.path.join(target_folder, 'modifier_plastic_generic_ceiling.json')
    Plastic.parse_file(file_path)


def test_modifier_plastic_generic_wall():
    file_path = os.path.join(target_folder, 'modifier_plastic_generic_wall.json')
    Plastic.parse_file(file_path)


def test_plastic_wrong():
    file_path = os.path.join(target_folder, 'modifier_plastic_black.json')
    with open(file_path) as json_file:
        plastic_modifier = json.load(json_file)

    # Test wrong type
    plastic_modifier_test = copy(plastic_modifier)
    plastic_modifier_test["type"] = 'glass'
    with pytest.raises(ValidationError):
        Plastic.parse_obj(plastic_modifier_test)

    # Test illegal character in identifier
    plastic_modifier_test = copy(plastic_modifier)
    plastic_modifier_test["identifier"] = '$#^&///'
    with pytest.raises(ValidationError):
        Plastic.parse_obj(plastic_modifier_test)

    # Test reflectance range
    plastic_modifier_test = copy(plastic_modifier)
    plastic_modifier_test["r_reflectance"] = -1
    with pytest.raises(ValidationError):
        Plastic.parse_obj(plastic_modifier_test)


def test_modifier_metal():
    file_path = os.path.join(target_folder, 'modifier_metal.json')
    Metal.parse_file(file_path)


def test_glass_generic_exterior_window():
    file_path = os.path.join(target_folder,
                             'modifier_glass_generic_exterior_window.json')
    Glass.parse_file(file_path)


def test_glass_air_boundary():
    file_path = os.path.join(target_folder,
                             'modifier_glass_air_boundary.json')
    Glass.parse_file(file_path)


def test_mirror_typical():
    file_path = os.path.join(target_folder, 'modifier_mirror_typical.json')
    Mirror.parse_file(file_path)

def test_mirror_invisible():
    file_path = os.path.join(target_folder, 'modifier_mirror_invisible.json')
    Mirror.parse_file(file_path)


def test_bsdf_klemsfull():
    file_path = os.path.join(target_folder, 'modifier_bsdf_klemsfull.json')
    BSDF.parse_file(file_path)


def test_modifier_glow_white():
    file_path = os.path.join(target_folder, 'modifier_glow_white.json')
    Glow.parse_file(file_path)


def test_modifier_light_green_spotlight():
    file_path = os.path.join(target_folder, 'modifier_light_green_spotlight.json')
    Light.parse_file(file_path)


def test_trans_tree_foliage():
    file_path = os.path.join(target_folder, 'modifier_trans_tree_foliage.json')
    Trans.parse_file(file_path)


def test_trans_tree_foliage_wrong():
    file_path = os.path.join(target_folder, 'modifier_trans_tree_foliage.json')
    with open(file_path) as json_file:
        trans_modifier = json.load(json_file)

    # Test wrong sum
    trans_modifier_test = copy(trans_modifier)
    trans_modifier_test["transmitted_diff"] = 0.6
    trans_modifier_test["transmitted_spec"] = 0.6
    with pytest.raises(ValidationError):
        Trans.parse_obj(trans_modifier_test)

