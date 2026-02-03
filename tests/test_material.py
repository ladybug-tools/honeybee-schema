from honeybee_schema.energy.material import EnergyMaterial, EnergyMaterialNoMass, \
    EnergyWindowMaterialGas, EnergyWindowMaterialGasMixture, \
    EnergyWindowMaterialGasCustom, EnergyWindowMaterialBlind, \
    EnergyWindowMaterialGlazing, EnergyWindowMaterialShade, \
    EnergyWindowMaterialSimpleGlazSys
from copy import copy
from pydantic import ValidationError
import pytest
import os
import json

# target folder where all of the samples live
root = os.path.dirname(os.path.dirname(__file__))
target_folder = os.path.join(root, 'samples', 'material')


def test_material_opaque_gypsum():
    file_path = os.path.join(target_folder, 'material_opaque_gypsum.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        EnergyMaterial.model_validate_json(f.read())


def test_material_opaque_insulation():
    file_path = os.path.join(target_folder, 'material_opaque_insulation.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        EnergyMaterial.model_validate_json(f.read())


def test_material_opaque_concrete():
    file_path = os.path.join(target_folder, 'material_opaque_concrete.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        EnergyMaterial.model_validate_json(f.read())


def test_material_opaque_brick():
    file_path = os.path.join(target_folder, 'material_opaque_brick.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        EnergyMaterial.model_validate_json(f.read())


def test_material_opaque_wall_gap():
    file_path = os.path.join(target_folder, 'material_opaque_wall_gap.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        EnergyMaterialNoMass.model_validate_json(f.read())


def material_window_glazing_clear():
    file_path = os.path.join(target_folder, 'material_window_glazing_clear.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        EnergyWindowMaterialGlazing.model_validate_json(f.read())


def material_window_glazing_lowe():
    file_path = os.path.join(target_folder, 'material_window_glazing_lowe.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        EnergyWindowMaterialGlazing.model_validate_json(f.read())


def test_material_window_blind():
    file_path = os.path.join(target_folder, 'material_window_blind.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        EnergyWindowMaterialBlind.model_validate_json(f.read())


def test_material_window_gas():
    file_path = os.path.join(target_folder, 'material_window_gas.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        EnergyWindowMaterialGas.model_validate_json(f.read())


def test_material_window_gas_mixture():
    file_path = os.path.join(target_folder, 'material_window_gas_mixture.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        EnergyWindowMaterialGasMixture.model_validate_json(f.read())


def test_material_window_gas_custom():
    file_path = os.path.join(target_folder, 'material_window_gas_custom.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        EnergyWindowMaterialGasCustom.model_validate_json(f.read())


def test_material_window_glazing_system():
    file_path = os.path.join(target_folder, 'material_window_glazing_system.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        EnergyWindowMaterialSimpleGlazSys.model_validate_json(f.read())


def test_material_window_shade():
    file_path = os.path.join(target_folder, 'material_window_shade.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        EnergyWindowMaterialShade.model_validate_json(f.read())


def test_material_wrong():
    file_path = os.path.join(target_folder, 'material_opaque_gypsum.json')
    with open(file_path) as json_file:
        material_gypsum = json.load(json_file)
    wrong_identifier = copy(material_gypsum)
    wrong_identifier['identifier'] = ''
    with pytest.raises(ValidationError):
        EnergyMaterial.model_validate(wrong_identifier)
    wrong_thickness = copy(material_gypsum)
    wrong_thickness['thickness'] = 5
    with pytest.raises(ValidationError):
        EnergyMaterial.model_validate(wrong_thickness)
    wrong_specificheat = copy(material_gypsum)
    wrong_specificheat['specific_heat'] = 0
    with pytest.raises(ValidationError):
        EnergyMaterial.model_validate(wrong_specificheat)


def test_materialnomass_wrong():
    file_path = os.path.join(target_folder, 'material_opaque_wall_gap.json')
    with open(file_path) as json_file:
        material_no_mass = json.load(json_file)
    wrong_r_value = copy(material_no_mass)
    wrong_r_value['r_value'] = 0
    with pytest.raises(ValidationError):
        EnergyMaterialNoMass.model_validate(wrong_r_value)
    wrong_solar_absorptance = copy(material_no_mass)
    wrong_solar_absorptance['solar_absorptance'] = 2
    with pytest.raises(ValidationError):
        EnergyMaterialNoMass.model_validate(wrong_solar_absorptance)


def test_window_simpleglaz_wrong():
    file_path = os.path.join(target_folder, 'material_window_glazing_system.json')
    with open(file_path) as json_file:
        window_simpleglazing = json.load(json_file)
    wrong_values = copy(window_simpleglazing)
    wrong_values['u_factor'] = 18
    with pytest.raises(ValidationError):
        EnergyWindowMaterialSimpleGlazSys.model_validate(wrong_values)
    wrong_values['shgc'] = 2
    with pytest.raises(ValidationError):
        EnergyWindowMaterialSimpleGlazSys.model_validate(wrong_values)


def test_windowshade_wrong():
    file_path = os.path.join(target_folder, 'material_window_shade.json')
    with open(file_path) as json_file:
        window_shade = json.load(json_file)
    wrong_type = copy(window_shade)
    wrong_type['type'] = 'EnergyWindowMaterial'
    with pytest.raises(ValidationError):
        EnergyWindowMaterialShade.model_validate(wrong_type)
    wrong_shadedistance = copy(window_shade)
    wrong_shadedistance['distance_to_glass'] = 0
    with pytest.raises(ValidationError):
        EnergyWindowMaterialShade.model_validate(wrong_shadedistance)
    wrong_airflow = copy(window_shade)
    wrong_airflow['airflow_permeability'] = 1
    with pytest.raises(ValidationError):
        EnergyWindowMaterialShade.model_validate(wrong_airflow)
