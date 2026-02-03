from honeybee_schema.model import Model
import os

# target folder where all of the samples live
root = os.path.dirname(os.path.dirname(__file__))
target_folder = os.path.join(root, 'samples', 'model')
target_folder_large = os.path.join(root, 'samples', 'model_large')


def validate_model(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        Model.model_validate_json(f.read())


def test_model_complete_multi_zone_office():
    file_path = os.path.join(target_folder, 'model_complete_multi_zone_office.hbjson')
    validate_model(file_path)


def test_model_complete_single_zone_office():
    file_path = os.path.join(target_folder, 'model_complete_single_zone_office.hbjson')
    validate_model(file_path)


def test_model_complete_user_data():
    file_path = os.path.join(target_folder, 'model_complete_user_data.hbjson')
    validate_model(file_path)


def test_model_complete_patient_room():
    file_path = os.path.join(target_folder, 'model_complete_patient_room.hbjson')
    validate_model(file_path)


def test_model_complete_multiroom_radiance():
    file_path = os.path.join(target_folder, 'model_complete_multiroom_radiance.hbjson')
    validate_model(file_path)


def test_model_radiance_grid_views():
    file_path = os.path.join(target_folder, 'model_radiance_grid_views.hbjson')
    validate_model(file_path)


def test_model_radiance_dynamic_states():
    file_path = os.path.join(target_folder, 'model_radiance_dynamic_states.hbjson')
    validate_model(file_path)


def test_model_energy_shoe_box():
    file_path = os.path.join(target_folder, 'model_energy_shoe_box.hbjson')
    validate_model(file_path)


def test_model_energy_detailed_loads():
    file_path = os.path.join(target_folder, 'model_energy_detailed_loads.hbjson')
    validate_model(file_path)


def test_model_energy_fixed_interval():
    file_path = os.path.join(target_folder, 'model_energy_fixed_interval.hbjson')
    validate_model(file_path)


def test_model_energy_no_program():
    file_path = os.path.join(target_folder, 'model_energy_no_program.hbjson')
    validate_model(file_path)


def test_model_energy_window_ventilation():
    file_path = os.path.join(target_folder, 'model_energy_window_ventilation.hbjson')
    validate_model(file_path)


def test_model_energy_afn():
    file_path = os.path.join(target_folder, 'model_energy_afn.hbjson')
    validate_model(file_path)


def test_model_energy_service_hot_water():
    file_path = os.path.join(target_folder, 'model_energy_service_hot_water.hbjson')
    validate_model(file_path)


def test_model_energy_allair_hvac():
    file_path = os.path.join(target_folder, 'model_energy_allair_hvac.hbjson')
    validate_model(file_path)


def test_model_energy_doas_hvac():
    file_path = os.path.join(target_folder, 'model_energy_doas_hvac.hbjson')
    validate_model(file_path)


def test_model_energy_window_ac():
    file_path = os.path.join(target_folder, 'model_energy_window_ac.hbjson')
    validate_model(file_path)


def test_model_5vertex_sub_faces():
    file_path = os.path.join(target_folder, 'model_5vertex_sub_faces.hbjson')
    validate_model(file_path)


def test_model_5vertex_sub_faces_interior():
    file_path = os.path.join(target_folder, 'model_5vertex_sub_faces_interior.hbjson')
    validate_model(file_path)


def test_model_with_shade_mesh():
    file_path = os.path.join(target_folder, 'model_with_shade_mesh.hbjson')
    validate_model(file_path)


def test_model_large_single_family_home():
    file_path = os.path.join(target_folder_large, 'single_family_home.hbjson')
    validate_model(file_path)


def test_model_large_lab_building():
    file_path = os.path.join(target_folder_large, 'lab_building.hbjson')
    validate_model(file_path)
