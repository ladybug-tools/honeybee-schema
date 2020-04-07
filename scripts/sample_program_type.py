# coding=utf-8
from __future__ import division

from honeybee_energy.load.infiltration import Infiltration

from honeybee_energy.lib.programtypes import office_program, plenum_program, \
    program_type_by_identifier

import os
import json


def program_type_abridged_plenum(directory):
    plenum = plenum_program.duplicate()
    infil = office_program.infiltration.duplicate()
    infil.identifier = 'Plenum Infiltration'
    plenum.infiltration = infil
    dest_file = os.path.join(directory, 'program_type_abridged_plenum.json')
    with open(dest_file, 'w') as fp:
        json.dump(plenum.to_dict(abridged=True), fp, indent=4)


def program_type_abridged_office(directory):
    dest_file = os.path.join(directory, 'program_type_abridged_office.json')
    with open(dest_file, 'w') as fp:
        json.dump(office_program.to_dict(abridged=True), fp, indent=4)


def program_type_abridged_kitchen(directory):
    kitchen = program_type_by_identifier(
        '2013::FullServiceRestaurant::Kitchen').duplicate()
    dest_file = os.path.join(directory, 'program_type_abridged_kitchen.json')
    with open(dest_file, 'w') as fp:
        json.dump(kitchen.to_dict(abridged=True), fp, indent=4)


def program_type_abridged_patient_room(directory):
    pat_room_program = program_type_by_identifier(
        '2013::Hospital::ICU_PatRm').duplicate()
    pat_room_program.setpoint.identifier = 'Humidity Controlled PatRm Setpt'
    pat_room_program.setpoint.heating_setpoint = 21
    pat_room_program.setpoint.cooling_setpoint = 24
    pat_room_program.setpoint.humidifying_setpoint = 30
    pat_room_program.setpoint.dehumidifying_setpoint = 55
    dest_file = os.path.join(directory, 'program_type_abridged_patient_room.json')
    with open(dest_file, 'w') as fp:
        json.dump(pat_room_program.to_dict(abridged=True), fp, indent=4)


def program_type_plenum(directory):
    plenum = plenum_program.duplicate()
    infil = office_program.infiltration.duplicate()
    infil.identifier = 'Plenum Infiltration'
    plenum.infiltration = infil
    dest_file = os.path.join(directory, 'program_type_plenum.json')
    with open(dest_file, 'w') as fp:
        json.dump(plenum.to_dict(abridged=False), fp, indent=4)


def program_type_office(directory):
    dest_file = os.path.join(directory, 'program_type_office.json')
    with open(dest_file, 'w') as fp:
        json.dump(office_program.to_dict(abridged=False), fp, indent=4)


# run all functions within the file
master_dir = os.path.split(os.path.dirname(__file__))[0]
sample_directory = os.path.join(master_dir, 'samples', 'program_type')

program_type_plenum(sample_directory)
program_type_office(sample_directory)
program_type_abridged_plenum(sample_directory)
program_type_abridged_office(sample_directory)
program_type_abridged_kitchen(sample_directory)
program_type_abridged_patient_room(sample_directory)
