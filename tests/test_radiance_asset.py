from honeybee_schema.radiance.asset import SensorGrid, View

import os
import json

# target folder where all of the samples live
root = os.path.dirname(os.path.dirname(__file__))
target_folder = os.path.join(root, 'samples', 'radiance_asset')


def test_sensor_grid_simple():
    file_path = os.path.join(target_folder, 'sensor_grid_simple.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        SensorGrid.model_validate_json(f.read())


def test_sensor_grid_detailed():
    file_path = os.path.join(target_folder, 'sensor_grid_detailed.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        SensorGrid.model_validate_json(f.read())


def test_view_perspective():
    file_path = os.path.join(target_folder, 'view_perspective.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        View.model_validate_json(f.read())


def test_view_parallel():
    file_path = os.path.join(target_folder, 'view_parallel.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        View.model_validate_json(f.read())
