from honeybee_schema.energy.hvac.idealair import IdealAirSystemAbridged
from honeybee_schema.energy.hvac.allair import VAV
from honeybee_schema.energy.hvac.doas import FCUwithDOASAbridged
from honeybee_schema.energy.hvac.heatcool import WindowAC
import os

# target folder where all of the samples live
root = os.path.dirname(os.path.dirname(__file__))
target_folder = os.path.join(root, 'samples', 'hvac')


def test_ideal_air_default():
    file_path = os.path.join(target_folder, 'ideal_air_default.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        IdealAirSystemAbridged.model_validate_json(f.read())


def test_ideal_air_detailed():
    file_path = os.path.join(target_folder, 'ideal_air_detailed.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        IdealAirSystemAbridged.model_validate_json(f.read())


def test_vav_template():
    file_path = os.path.join(target_folder, 'vav_template.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        VAV.model_validate_json(f.read())


def test_fcu_with_doas_template():
    file_path = os.path.join(target_folder, 'fcu_with_doas_template.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        FCUwithDOASAbridged.model_validate_json(f.read())


def test_window_ac_with_baseboard_template():
    file_path = os.path.join(target_folder, 'window_ac_with_baseboard_template.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        WindowAC.model_validate_json(f.read())
