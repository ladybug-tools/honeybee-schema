from honeybee_model_schema.energy.load import LightingAbridged
import os

# target folder where all of the samples live
root = os.path.dirname(os.path.dirname(__file__))
target_folder = os.path.join(root, 'honeybee_model_schema', 'samples')

def test_lighting():
    file_path = os.path.join(
        target_folder, 'lighting_abridged.json')
    LightingAbridged.parse_file(file_path)
