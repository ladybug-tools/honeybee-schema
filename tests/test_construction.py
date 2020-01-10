from honeybee_schema.energy.construction import OpaqueConstructionAbridged, \
        WindowConstructionAbridged
from copy import copy
from pydantic import ValidationError
import pytest
import os
import json

# target folder where all of the samples live
root = os.path.dirname(os.path.dirname(__file__))
target_folder = os.path.join(root, 'honeybee_schema', 'samples')


def test_construction_window():
    file_path = os.path.join(target_folder, 'construction_window.json')
    WindowConstructionAbridged.parse_file(file_path)


def test_construction_window2():
    file_path = os.path.join(target_folder, 'construction_window2.json')
    WindowConstructionAbridged.parse_file(file_path)


def test_construction_window_blind():
    file_path = os.path.join(target_folder, 'construction_window_blind.json')
    WindowConstructionAbridged.parse_file(file_path)


def test_construction_opaqueroof():
    file_path = os.path.join(target_folder, 'construction_roof.json')
    OpaqueConstructionAbridged.parse_file(file_path)


def test_construction_opaquewall():
    file_path = os.path.join(target_folder, 'construction_wall.json')
    OpaqueConstructionAbridged.parse_file(file_path)


def test_construction_internal_floor():
    file_path = os.path.join(target_folder, 'construction_internal_floor.json')
    OpaqueConstructionAbridged.parse_file(file_path)


def test_length_opaque():
    file_path = os.path.join(target_folder, 'construction_internal_floor.json')
    with open(file_path) as json_file:
        construction_internal_floor = json.load(json_file)
    cons_length_test = copy(construction_internal_floor)
    for i in range(10):
        cons_length_test['layers'].append('material_{}'.format(i))
    with pytest.raises(ValidationError):
        OpaqueConstructionAbridged.parse_obj(cons_length_test)
    cons_length_test['layers'] = []
    with pytest.raises(ValidationError):
        OpaqueConstructionAbridged.parse_obj(cons_length_test)


def test_cons_wind():
    file_path = os.path.join(target_folder, 'construction_window.json')
    with open(file_path) as json_file:
        construction_window = json.load(json_file)
    cons_length_test = copy(construction_window)
    for i in range(8):
        cons_length_test['layers'].append('material_{}'.format(i))
    with pytest.raises(ValidationError):
        WindowConstructionAbridged.parse_obj(cons_length_test)
    cons_length_test['layers'] = []
    with pytest.raises(ValidationError):
        WindowConstructionAbridged.parse_obj(cons_length_test)
