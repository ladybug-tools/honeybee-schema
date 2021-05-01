from honeybee_schema.energy.daylight import DaylightingControl
import os

# target folder where all of the samples live
root = os.path.dirname(os.path.dirname(__file__))
target_folder = os.path.join(root, 'samples', 'daylight')


def test_daylight_control():
    file_path = os.path.join(target_folder, 'daylight_control.json')
    DaylightingControl.parse_file(file_path)
