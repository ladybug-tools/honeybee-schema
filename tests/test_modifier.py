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
    with open(file_path, 'r', encoding='utf-8') as f:
        Plastic.model_validate_json(f.read())


def test_modifier_plastic_generic_ceiling():
    file_path = os.path.join(target_folder, 'modifier_plastic_generic_ceiling.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        Plastic.model_validate_json(f.read())


def test_modifier_plastic_generic_wall():
    file_path = os.path.join(target_folder, 'modifier_plastic_generic_wall.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        Plastic.model_validate_json(f.read())


def test_plastic_wrong():
    file_path = os.path.join(target_folder, 'modifier_plastic_black.json')
    with open(file_path, 'r', encoding='utf-8') as json_file:
        plastic_modifier = json.load(json_file)

    # Test wrong type
    plastic_modifier_test = copy(plastic_modifier)
    plastic_modifier_test["type"] = 'glass'
    with pytest.raises(ValidationError):
        Plastic.model_validate(plastic_modifier_test)

    # Test illegal character in identifier
    plastic_modifier_test = copy(plastic_modifier)
    plastic_modifier_test["identifier"] = '$#^&///'
    with pytest.raises(ValidationError):
        Plastic.model_validate(plastic_modifier_test)

    # Test reflectance range
    plastic_modifier_test = copy(plastic_modifier)
    plastic_modifier_test["r_reflectance"] = -1
    with pytest.raises(ValidationError):
        Plastic.model_validate(plastic_modifier_test)


def test_modifier_metal():
    file_path = os.path.join(target_folder, 'modifier_metal.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        Metal.model_validate_json(f.read())


def test_glass_generic_exterior_window():
    file_path = os.path.join(
        target_folder, 'modifier_glass_generic_exterior_window.json'
    )
    with open(file_path, 'r', encoding='utf-8') as f:
        Glass.model_validate_json(f.read())


def test_glass_air_boundary():
    file_path = os.path.join(
        target_folder, 'modifier_glass_air_boundary.json'
    )
    with open(file_path, 'r', encoding='utf-8') as f:
        Glass.model_validate_json(f.read())


def test_mirror_typical():
    file_path = os.path.join(target_folder, 'modifier_mirror_typical.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        Mirror.model_validate_json(f.read())


def test_mirror_invisible():
    file_path = os.path.join(target_folder, 'modifier_mirror_invisible.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        Mirror.model_validate_json(f.read())


def test_bsdf_klemsfull():
    file_path = os.path.join(target_folder, 'modifier_bsdf_klemsfull.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        BSDF.model_validate_json(f.read())


def test_modifier_glow_white():
    file_path = os.path.join(target_folder, 'modifier_glow_white.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        Glow.model_validate_json(f.read())


def test_modifier_light_green_spotlight():
    file_path = os.path.join(
        target_folder, 'modifier_light_green_spotlight.json'
    )
    with open(file_path, 'r', encoding='utf-8') as f:
        Light.model_validate_json(f.read())


def test_trans_tree_foliage():
    file_path = os.path.join(
        target_folder, 'modifier_trans_tree_foliage.json'
    )
    with open(file_path, 'r', encoding='utf-8') as f:
        Trans.model_validate_json(f.read())


def test_trans_tree_foliage_wrong():
    file_path = os.path.join(
        target_folder, 'modifier_trans_tree_foliage.json'
    )
    with open(file_path, 'r', encoding='utf-8') as json_file:
        trans_modifier = json.load(json_file)

    # Test wrong sum (this one does NOT expect a ValidationError)
    trans_modifier_test = copy(trans_modifier)
    trans_modifier_test["transmitted_diff"] = 0.6
    trans_modifier_test["transmitted_spec"] = 0.6
    Trans.model_validate(trans_modifier_test)
