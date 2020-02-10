from honeybee_schema.energy.hvac import IdealAirSystemAbridged
import os

# target folder where all of the samples live
root = os.path.dirname(os.path.dirname(__file__))
target_folder = os.path.join(root, 'samples', 'hvac')


def test_ideal_air_default():
    file_path = os.path.join(target_folder, 'ideal_air_default.json')
    IdealAirSystemAbridged.parse_file(file_path)


def test_ideal_air_detailed():
    file_path = os.path.join(target_folder, 'ideal_air_detailed.json')
    IdealAirSystemAbridged.parse_file(file_path)
