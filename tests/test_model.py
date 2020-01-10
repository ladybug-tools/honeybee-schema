from honeybee_schema.model import Model
import os

# target folder where all of the samples live
root = os.path.dirname(os.path.dirname(__file__))
target_folder = os.path.join(root, 'honeybee_schema', 'samples')


def test_model_multi_zone_single_family_house():
    file_path  = os.path.join(target_folder, 'model_multi_zone_single_family_house.json')
    Model.parse_file(file_path)

def test_model_shoe_box():
    file_path  = os.path.join(target_folder, 'model_shoe_box.json')
    Model.parse_file(file_path)

def test_model_single_zone_tiny_house():
    file_path  = os.path.join(target_folder, 'model_single_zone_tiny_house.json')
    Model.parse_file(file_path)

def test_model_multi_zone_office():
    file_path  = os.path.join(target_folder, 'model_complete_multi_zone_office.json')
    Model.parse_file(file_path)

def test_model_single_zone_office():
    file_path  = os.path.join(target_folder, 'model_complete_single_zone_office.json')
    Model.parse_file(file_path)

def test_model_single_zone_office_detailed_loads():
    file_path  = os.path.join(target_folder, 'model_complete_single_zone_office_detailed_loads.json')
    Model.parse_file(file_path) 

def test_model_with_humidity_setpoints():
    file_path  = os.path.join(target_folder, 'model_complete_with_humidity_setpoints.json')
    Model.parse_file(file_path) 
  