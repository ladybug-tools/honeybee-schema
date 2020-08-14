from honeybee_schema.energy.ventcool import VentilationControlAbridged, \
    VentilationOpening, VentilationSimulationControl, AFNCrack

import os

# target folder where all of the samples live
root = os.path.dirname(os.path.dirname(__file__))
target_folder = os.path.join(root, 'samples', 'ventcool')


def test_ventilation_opening_default():
    file_path = os.path.join(target_folder, 'ventilation_opening_default.json')
    VentilationOpening.parse_file(file_path)


def test_ventilation_control_simple():
    file_path = os.path.join(target_folder, 'ventilation_control_simple.json')
    VentilationControlAbridged.parse_file(file_path)


def test_ventilation_control_detailed():
    file_path = os.path.join(target_folder, 'ventilation_control_detailed.json')
    VentilationControlAbridged.parse_file(file_path)


def test_ventilation_crack():
    file_path = os.path.join(target_folder, 'ventilation_crack.json')
    AFNCrack.parse_file(file_path)


def ventilation_simulation_control(directory):
    file_path = os.path.join(target_folder, 'ventilation_simulation_control.json')
    VentilationSimulationControl.parse_file(file_path)
