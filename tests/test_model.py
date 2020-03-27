from honeybee_schema.model import Model
from honeybee_schema.energy.properties import ModelEnergyProperties
import os

# target folder where all of the samples live
root = os.path.dirname(os.path.dirname(__file__))
target_folder = os.path.join(root, 'samples', 'model')


def test_model_complete_multi_zone_office():
    file_path  = os.path.join(target_folder, 'model_complete_multi_zone_office.json')
    Model.parse_file(file_path)


def test_model_complete_single_zone_office():
    file_path  = os.path.join(target_folder, 'model_complete_single_zone_office.json')
    Model.parse_file(file_path)


def test_model_complete_user_data():
    file_path  = os.path.join(target_folder, 'model_complete_user_data.json')
    Model.parse_file(file_path)


def test_model_complete_patient_room():
    file_path  = os.path.join(target_folder, 'model_complete_patient_room.json')
    Model.parse_file(file_path) 


def test_model_energy_shoe_box():
    file_path  = os.path.join(target_folder, 'model_energy_shoe_box.json')
    Model.parse_file(file_path)


def test_model_energy_detailed_loads():
    file_path  = os.path.join(target_folder, 'model_energy_detailed_loads.json')
    Model.parse_file(file_path) 


def test_model_energy_fixed_interval():
    file_path  = os.path.join(target_folder, 'model_energy_fixed_interval.json')
    Model.parse_file(file_path)


def test_model_energy_no_program():
    file_path  = os.path.join(target_folder, 'model_energy_no_program.json')
    Model.parse_file(file_path)


def test_model_energy_properties_office():
    file_path  = os.path.join(target_folder, 'model_energy_properties_office.json')
    ModelEnergyProperties.parse_file(file_path)
