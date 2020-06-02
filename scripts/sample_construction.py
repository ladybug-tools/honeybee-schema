# coding=utf-8
from __future__ import division

from honeybee_energy.construction.window import WindowConstruction
from honeybee_energy.construction.windowshade import WindowConstructionShade
from honeybee_energy.material.shade import EnergyWindowMaterialBlind, \
    EnergyWindowMaterialShade

from honeybee_energy.lib.materials import lowe_glass, clear_glass, argon_gap
from honeybee_energy.lib.constructions import generic_exterior_wall, \
    generic_roof, generic_exterior_door, generic_double_pane

import os
import json


def construction_opaque_door(directory):
    dest_file = os.path.join(directory, 'construction_opaque_door.json')
    with open(dest_file, 'w') as fp:
        json.dump(generic_exterior_door.to_dict(abridged=True), fp, indent=4)


def construction_opaque_roof(directory):
    dest_file = os.path.join(directory, 'construction_opaque_roof.json')
    with open(dest_file, 'w') as fp:
        json.dump(generic_roof.to_dict(abridged=True), fp, indent=4)


def construction_opaque_wall(directory):
    dest_file = os.path.join(directory, 'construction_opaque_wall.json')
    with open(dest_file, 'w') as fp:
        json.dump(generic_exterior_wall.to_dict(abridged=True), fp, indent=4)


def construction_window_double(directory):
    dest_file = os.path.join(directory, 'construction_window_double.json')
    with open(dest_file, 'w') as fp:
        json.dump(generic_double_pane.to_dict(abridged=True), fp, indent=4)


def construction_window_triple(directory):
    triple_pane = WindowConstruction(
        'Triple Pane Argon', [lowe_glass, argon_gap, lowe_glass, argon_gap, clear_glass])
    dest_file = os.path.join(directory, 'construction_window_triple.json')
    with open(dest_file, 'w') as fp:
        json.dump(triple_pane.to_dict(abridged=True), fp, indent=4)


def construction_window_blinds(directory):
    shade_mat = EnergyWindowMaterialBlind(
        'Plastic Blind', 'Vertical', 0.025, 0.01875, 0.003, 90, 0.2, 0.05, 0.4,
        0.05, 0.45, 0, 0.95, 0.1, 1)
    window_constr = WindowConstruction('Double Low-E', [lowe_glass, argon_gap, clear_glass])
    window_with_blinds = WindowConstructionShade(
        'Double Low-E Outside Shade', window_constr, shade_mat, 'Interior')
    dest_file = os.path.join(directory, 'construction_window_blinds.json')
    with open(dest_file, 'w') as fp:
        json.dump(window_with_blinds.to_dict(abridged=True), fp, indent=4)


def construction_window_shade(directory):
    """Test the initialization of WindowConstructionShade objects with shades."""
    shade_mat = EnergyWindowMaterialShade(
        'Low-e Diffusing Shade', 0.025, 0.15, 0.5, 0.25, 0.5, 0, 0.4,
        0.2, 0.1, 0.75, 0.25)
    window_constr = WindowConstruction('Double Low-E', [lowe_glass, argon_gap, clear_glass])
    window_with_shade = WindowConstructionShade(
        'Double Low-E Outside Shade', window_constr, shade_mat, 'Interior')
    dest_file = os.path.join(directory, 'construction_window_shade.json')
    with open(dest_file, 'w') as fp:
        json.dump(window_with_shade.to_dict(abridged=True), fp, indent=4)


# run all functions within the file
master_dir = os.path.split(os.path.dirname(__file__))[0]
sample_directory = os.path.join(master_dir, 'samples', 'construction')

construction_opaque_door(sample_directory)
construction_opaque_roof(sample_directory)
construction_opaque_wall(sample_directory)
construction_window_double(sample_directory)
construction_window_triple(sample_directory)
construction_window_blinds(sample_directory)
construction_window_shade(sample_directory)
