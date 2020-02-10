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
    EnergyMaterial.parse_file(file_path)


def test_material_opaque_insulation():
    file_path = os.path.join(target_folder, 'material_opaque_insulation.json')
    EnergyMaterial.parse_file(file_path)


def test_material_opaque_concrete():
    file_path = os.path.join(target_folder, 'material_opaque_concrete.json')
    EnergyMaterial.parse_file(file_path)


def test_material_opaque_brick():
    file_path = os.path.join(target_folder, 'material_opaque_brick.json')
    EnergyMaterial.parse_file(file_path)


def test_material_opaque_wall_gap():
    file_path = os.path.join(target_folder, 'material_opaque_wall_gap.json')
    EnergyMaterialNoMass.parse_file(file_path)


def material_window_glazing_clear():
    file_path = os.path.join(target_folder, 'material_window_glazing_clear.json')
    EnergyWindowMaterialGlazing.parse_file(file_path)


def material_window_glazing_lowe():
    file_path = os.path.join(target_folder, 'material_window_glazing_lowe.json')
    EnergyWindowMaterialGlazing.parse_file(file_path)


def test_material_window_blind():
    file_path = os.path.join(target_folder, 'material_window_blind.json')
    EnergyWindowMaterialBlind.parse_file(file_path)


def test_material_window_gas():
    file_path = os.path.join(target_folder, 'material_window_gas.json')
    EnergyWindowMaterialGas.parse_file(file_path)


def test_material_window_gas_mixture():
    file_path = os.path.join(target_folder, 'material_window_gas_mixture.json')
    EnergyWindowMaterialGasMixture.parse_file(file_path)


def test_material_window_gas_custom():
    file_path = os.path.join(target_folder, 'material_window_gas_custom.json')
    EnergyWindowMaterialGasCustom.parse_file(file_path)


def test_material_window_glazing_system():
    file_path = os.path.join(target_folder, 'material_window_glazing_system.json')
    EnergyWindowMaterialSimpleGlazSys.parse_file(file_path)


def test_material_window_shade():
    file_path = os.path.join(target_folder, 'material_window_shade.json')
    EnergyWindowMaterialShade.parse_file(file_path)


def test_material_wrong():
    file_path = os.path.join(target_folder, 'material_opaque_gypsum.json')
    with open(file_path) as json_file:
        material_gypsum = json.load(json_file)
    wrong_name = copy(material_gypsum)
    wrong_name['name'] = ''
    with pytest.raises(ValidationError):
        EnergyMaterial.parse_obj(wrong_name)
    wrong_thickness = copy(material_gypsum)
    wrong_thickness['thickness'] = 5
    with pytest.raises(ValidationError):
        EnergyMaterial.parse_obj(wrong_thickness)
    wrong_specificheat = copy(material_gypsum)
    wrong_specificheat['specific_heat'] = 0
    with pytest.raises(ValidationError):
        EnergyMaterial.parse_obj(wrong_specificheat)


def test_materialnomass_wrong():
    file_path = os.path.join(target_folder, 'material_opaque_wall_gap.json')
    with open(file_path) as json_file:
        material_no_mass = json.load(json_file)
    wrong_r_value = copy(material_no_mass)
    wrong_r_value['r_value'] = 0
    with pytest.raises(ValidationError):
        EnergyMaterialNoMass.parse_obj(wrong_r_value)
    wrong_solar_absorptance = copy(material_no_mass)
    wrong_solar_absorptance['solar_absorptance'] = 2
    with pytest.raises(ValidationError):
        EnergyMaterialNoMass.parse_obj(wrong_solar_absorptance)


def test_window_simpleglaz_wrong():
    file_path = os.path.join(target_folder, 'material_window_glazing_system.json')
    with open(file_path) as json_file:
        window_simpleglazing = json.load(json_file)
    wrong_values = copy(window_simpleglazing)
    wrong_values['u_factor'] = 6
    with pytest.raises(ValidationError):
        EnergyWindowMaterialSimpleGlazSys.parse_obj(wrong_values)
    wrong_values['SHGC'] = 2
    with pytest.raises(ValidationError):
        EnergyWindowMaterialSimpleGlazSys.parse_obj(wrong_values)


def test_windowshade_wrong():
    file_path = os.path.join(target_folder, 'material_window_shade.json')
    with open(file_path) as json_file:
        window_shade = json.load(json_file)
    wrong_type = copy(window_shade)
    wrong_type['type'] = 'EnergyWindowMaterial'
    with pytest.raises(ValidationError):
        EnergyWindowMaterialShade.parse_obj(wrong_type)
    wrong_shadedistance = copy(window_shade)
    wrong_shadedistance['distance_to_glass'] = 0
    with pytest.raises(ValidationError):
        EnergyWindowMaterialShade.parse_obj(wrong_shadedistance)
    wrong_airflow = copy(window_shade)
    wrong_airflow['airflow_permeability'] = 1
    with pytest.raises(ValidationError):
        EnergyWindowMaterialShade.parse_obj(wrong_airflow)
