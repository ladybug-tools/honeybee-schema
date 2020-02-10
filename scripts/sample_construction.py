# coding=utf-8
from __future__ import division

from honeybee_energy.construction.window import WindowConstruction
from honeybee_energy.material.shade import EnergyWindowMaterialBlind

from  honeybee_energy.lib.materials import lowe_glass, clear_glass, argon_gap
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
    blinds = EnergyWindowMaterialBlind('Generic Aluminium Blinds')
    window_with_blinds = WindowConstruction(
        'Triple Pane Argon', [lowe_glass, argon_gap, lowe_glass, blinds])
    dest_file = os.path.join(directory, 'construction_window_blinds.json')
    with open(dest_file, 'w') as fp:
        json.dump(window_with_blinds.to_dict(abridged=True), fp, indent=4)


# run all functions within the file
master_dir = os.path.split(os.path.dirname(__file__))[0]
sample_directory = os.path.join(master_dir, 'samples', 'construction')

construction_opaque_door(sample_directory)
construction_opaque_roof(sample_directory)
construction_opaque_wall(sample_directory)
construction_window_double(sample_directory)
construction_window_triple(sample_directory)
construction_window_blinds(sample_directory)
