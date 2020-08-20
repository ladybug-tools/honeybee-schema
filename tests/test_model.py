from honeybee_schema.model import Model
from honeybee_schema.energy.properties import ModelEnergyProperties
import os

# target folder where all of the samples live
root = os.path.dirname(os.path.dirname(__file__))
target_folder = os.path.join(root, 'samples', 'model')
target_folder_large = os.path.join(root, 'samples', 'model_large')


def test_model_complete_multi_zone_office():
    file_path = os.path.join(target_folder, 'model_complete_multi_zone_office.json')
    Model.parse_file(file_path)


def test_model_complete_single_zone_office():
    file_path = os.path.join(target_folder, 'model_complete_single_zone_office.json')
    Model.parse_file(file_path)


def test_model_complete_user_data():
    file_path = os.path.join(target_folder, 'model_complete_user_data.json')
    Model.parse_file(file_path)


def test_model_complete_patient_room():
    file_path = os.path.join(target_folder, 'model_complete_patient_room.json')
    Model.parse_file(file_path)


def test_model_complete_multiroom_radiance():
    file_path = os.path.join(target_folder, 'model_complete_multiroom_radiance.json')
    Model.parse_file(file_path)


def test_model_radiance_grid_views():
    file_path = os.path.join(target_folder, 'model_radiance_grid_views.json')
    Model.parse_file(file_path)


def test_model_radiance_dynamic_states():
    file_path = os.path.join(target_folder, 'model_radiance_dynamic_states.json')
    Model.parse_file(file_path)


def test_model_energy_shoe_box():
    file_path = os.path.join(target_folder, 'model_energy_shoe_box.json')
    Model.parse_file(file_path)


def test_model_energy_detailed_loads():
    file_path = os.path.join(target_folder, 'model_energy_detailed_loads.json')
    Model.parse_file(file_path)


def test_model_energy_fixed_interval():
    file_path = os.path.join(target_folder, 'model_energy_fixed_interval.json')
    Model.parse_file(file_path)


def test_model_energy_no_program():
    file_path = os.path.join(target_folder, 'model_energy_no_program.json')
    Model.parse_file(file_path)


def test_model_energy_window_ventilation():
    file_path = os.path.join(target_folder, 'model_energy_window_ventilation.json')
    Model.parse_file(file_path)


def test_model_energy_afn():
    file_path = os.path.join(target_folder, 'model_energy_afn.json')
    Model.parse_file(file_path)


def test_model_energy_allair_hvac():
    file_path = os.path.join(target_folder, 'model_energy_allair_hvac.json')
    Model.parse_file(file_path)


def test_model_energy_doas_hvac():
    file_path = os.path.join(target_folder, 'model_energy_doas_hvac.json')
    Model.parse_file(file_path)


def test_model_energy_window_ac():
    file_path = os.path.join(target_folder, 'model_energy_window_ac.json')
    Model.parse_file(file_path)


def test_model_5vertex_sub_faces():
    file_path = os.path.join(target_folder, 'model_5vertex_sub_faces.json')
    Model.parse_file(file_path)


def test_model_5vertex_sub_faces_interior():
    file_path = os.path.join(target_folder, 'model_5vertex_sub_faces_interior.json')
    Model.parse_file(file_path)


def test_model_energy_properties_office():
    file_path = os.path.join(target_folder, 'model_energy_properties_office.json')
    ModelEnergyProperties.parse_file(file_path)


def test_model_large_single_family_home():
    file_path = os.path.join(target_folder_large, 'single_family_home.json')
    Model.parse_file(file_path)


def test_model_large_lab_building():
    file_path = os.path.join(target_folder_large, 'lab_building.json')
    Model.parse_file(file_path)
