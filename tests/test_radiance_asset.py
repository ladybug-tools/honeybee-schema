from honeybee_schema.radiance.asset import SensorGrid, View

import os
import json

# target folder where all of the samples live
root = os.path.dirname(os.path.dirname(__file__))
target_folder = os.path.join(root, 'samples', 'radiance_asset')


def test_sensor_grid_simple():
    file_path = os.path.join(target_folder, 'sensor_grid_simple.json')
    SensorGrid.parse_file(file_path)


def test_sensor_grid_detailed():
    file_path = os.path.join(target_folder, 'sensor_grid_detailed.json')
    SensorGrid.parse_file(file_path)


def test_view_perspective():
    file_path = os.path.join(target_folder, 'view_perspective.json')
    View.parse_file(file_path)


def test_view_parallel():
    file_path = os.path.join(target_folder, 'view_parallel.json')
    View.parse_file(file_path)
