
# coding=utf-8
from __future__ import division

from honeybee_radiance.sensor import Sensor
from honeybee_radiance.sensorgrid import SensorGrid
from honeybee_radiance.view import View

from honeybee.room import Room

import os
import json


def sensor_grid_simple(directory):
    sensors = [Sensor((0, 0, 0), (0, 0, 1)), Sensor((0, 0, 10), (0, 0, 1))]
    sg = SensorGrid('sg_1', sensors)
    dest_file = os.path.join(directory, 'sensor_grid_simple.json')
    with open(dest_file, 'w') as fp:
        json.dump(sg.to_dict(), fp, indent=4)


def sensor_grid_detailed(directory):
    room1 = Room.from_box('Tiny_House_Room', 5, 10, 3)
    sensor_grid = room1.properties.radiance.generate_sensor_grid(1, 1, 1)
    sensor_grid.display_name = 'Tiny House Sensor Grid'
    dest_file = os.path.join(directory, 'sensor_grid_detailed.json')
    with open(dest_file, 'w') as fp:
        json.dump(sensor_grid.to_dict(), fp, indent=4)


def view_perspective(directory):
    vw = View('test_view_perspective', (0, 0, 10), (0, 1, 0), (0, 0, 1))
    dest_file = os.path.join(directory, 'view_perspective.json')
    with open(dest_file, 'w') as fp:
        json.dump(vw.to_dict(), fp, indent=4)


def view_parallel(directory):
    vw = View('test_view', (0, 0, 10), (0, 1, 0), (0, 0, 1), 'l', 240, 300, -10, -25)
    dest_file = os.path.join(directory, 'view_parallel.json')
    with open(dest_file, 'w') as fp:
        json.dump(vw.to_dict(), fp, indent=4)


# run all functions within the file
master_dir = os.path.split(os.path.dirname(__file__))[0]
sample_directory = os.path.join(master_dir, 'samples', 'radiance_asset')

sensor_grid_simple(sample_directory)
sensor_grid_detailed(sample_directory)
view_perspective(sample_directory)
view_parallel(sample_directory)
