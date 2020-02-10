# coding=utf-8
from __future__ import division

from honeybee_energy.material.opaque import EnergyMaterialNoMass
from honeybee_energy.material.glazing import EnergyWindowMaterialSimpleGlazSys
from honeybee_energy.material.gas import EnergyWindowMaterialGasMixture, \
    EnergyWindowMaterialGasCustom
from honeybee_energy.material.shade import EnergyWindowMaterialShade, \
    EnergyWindowMaterialBlind

from  honeybee_energy.lib.materials import brick, concrete_lw, insulation, gypsum, \
    lowe_glass, clear_glass, air_gap

import os
import json


def material_opaque_brick(directory):
    dest_file = os.path.join(directory, 'material_opaque_brick.json')
    with open(dest_file, 'w') as fp:
        json.dump(brick.to_dict(), fp, indent=4)


def material_opaque_concrete(directory):
    dest_file = os.path.join(directory, 'material_opaque_concrete.json')
    with open(dest_file, 'w') as fp:
        json.dump(concrete_lw.to_dict(), fp, indent=4)


def material_opaque_insulation(directory):
    dest_file = os.path.join(directory, 'material_opaque_insulation.json')
    with open(dest_file, 'w') as fp:
        json.dump(insulation.to_dict(), fp, indent=4)


def material_opaque_gypsum(directory):
    dest_file = os.path.join(directory, 'material_opaque_gypsum.json')
    with open(dest_file, 'w') as fp:
        json.dump(gypsum.to_dict(), fp, indent=4)


def material_opaque_wall_gap(directory):
    wall_gap = EnergyMaterialNoMass('Generic Wall Air Gap', 0.15, roughness='Smooth')
    dest_file = os.path.join(directory, 'material_opaque_wall_gap.json')
    with open(dest_file, 'w') as fp:
        json.dump(wall_gap.to_dict(), fp, indent=4)


def material_window_glazing_clear(directory):
    dest_file = os.path.join(directory, 'material_window_glazing_clear.json')
    with open(dest_file, 'w') as fp:
        json.dump(clear_glass.to_dict(), fp, indent=4)


def material_window_glazing_lowe(directory):
    dest_file = os.path.join(directory, 'material_window_glazing_lowe.json')
    with open(dest_file, 'w') as fp:
        json.dump(lowe_glass.to_dict(), fp, indent=4)


def material_window_gas(directory):
    dest_file = os.path.join(directory, 'material_window_gas.json')
    with open(dest_file, 'w') as fp:
        json.dump(air_gap.to_dict(), fp, indent=4)


def material_window_gas_mixture(directory):
    argon_mix = EnergyWindowMaterialGasMixture(
        'Argon Air Mixture', 0.0125, ['Argon', 'Air'], [0.9, 0.1])
    dest_file = os.path.join(directory, 'material_window_gas_mixture.json')
    with open(dest_file, 'w') as fp:
        json.dump(argon_mix.to_dict(), fp, indent=4)


def material_window_gas_custom(directory):
    co2_gap = EnergyWindowMaterialGasCustom('CO2', 0.0125, 0.0146, 0.000014, 827.73)
    co2_gap.specific_heat_ratio = 1.4
    co2_gap.molecular_weight = 44
    dest_file = os.path.join(directory, 'material_window_gas_custom.json')
    with open(dest_file, 'w') as fp:
        json.dump(co2_gap.to_dict(), fp, indent=4)


def material_window_glazing_system(directory):
    simple_sys = EnergyWindowMaterialSimpleGlazSys(
        'Fixed Window 2.00 0.40 0.31', u_factor=1.98, shgc=0.4)
    dest_file = os.path.join(directory, 'material_window_glazing_system.json')
    with open(dest_file, 'w') as fp:
        json.dump(simple_sys.to_dict(), fp, indent=4)


def material_window_blind(directory):
    blinds = EnergyWindowMaterialBlind('Generic Aluminium Blinds')
    dest_file = os.path.join(directory, 'material_window_blind.json')
    with open(dest_file, 'w') as fp:
        json.dump(blinds.to_dict(), fp, indent=4)


def material_window_shade(directory):
    shades = EnergyWindowMaterialShade('White Diffusing Roller Shade')
    dest_file = os.path.join(directory, 'material_window_shade.json')
    with open(dest_file, 'w') as fp:
        json.dump(shades.to_dict(), fp, indent=4)


# run all functions within the file
master_dir = os.path.split(os.path.dirname(__file__))[0]
sample_directory = os.path.join(master_dir, 'samples', 'material')

material_opaque_brick(sample_directory)
material_opaque_concrete(sample_directory)
material_opaque_insulation(sample_directory)
material_opaque_gypsum(sample_directory)
material_opaque_wall_gap(sample_directory)
material_window_glazing_clear(sample_directory)
material_window_glazing_lowe(sample_directory)
material_window_gas(sample_directory)
material_window_gas_mixture(sample_directory)
material_window_gas_custom(sample_directory)
material_window_glazing_system(sample_directory)
material_window_blind(sample_directory)
material_window_shade(sample_directory)
