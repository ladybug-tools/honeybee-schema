from honeybee_schema.energy.construction import OpaqueConstructionAbridged, \
    WindowConstructionAbridged, WindowConstructionShadeAbridged
from copy import copy
from pydantic import ValidationError
import pytest
import os
import json

# target folder where all of the samples live
root = os.path.dirname(os.path.dirname(__file__))
target_folder = os.path.join(root, 'samples', 'construction')


def test_construction_window_double():
    file_path = os.path.join(target_folder, 'construction_window_double.json')
    WindowConstructionAbridged.parse_file(file_path)


def test_construction_window_triple():
    file_path = os.path.join(target_folder, 'construction_window_triple.json')
    WindowConstructionAbridged.parse_file(file_path)


def test_construction_opaque_door():
    file_path = os.path.join(target_folder, 'construction_opaque_door.json')
    OpaqueConstructionAbridged.parse_file(file_path)


def test_construction_opaque_roof():
    file_path = os.path.join(target_folder, 'construction_opaque_roof.json')
    OpaqueConstructionAbridged.parse_file(file_path)


def test_construction_opaque_wall():
    file_path = os.path.join(target_folder, 'construction_opaque_wall.json')
    OpaqueConstructionAbridged.parse_file(file_path)


def test_construction_window_shade():
    file_path = os.path.join(target_folder, 'construction_window_shade.json')
    WindowConstructionShadeAbridged.parse_file(file_path)


def test_construction_window_blinds():
    file_path = os.path.join(target_folder, 'construction_window_blinds.json')
    WindowConstructionShadeAbridged.parse_file(file_path)


def test_length_opaque():
    file_path = os.path.join(target_folder, 'construction_opaque_wall.json')
    with open(file_path) as json_file:
        construction_wall = json.load(json_file)
    cons_length_test = copy(construction_wall)
    for i in range(10):
        cons_length_test['layers'].append('material_{}'.format(i))
    with pytest.raises(ValidationError):
        OpaqueConstructionAbridged.parse_obj(cons_length_test)
    cons_length_test['layers'] = []
    with pytest.raises(ValidationError):
        OpaqueConstructionAbridged.parse_obj(cons_length_test)


def test_length_window():
    file_path = os.path.join(target_folder, 'construction_window_double.json')
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
