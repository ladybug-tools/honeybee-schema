# coding=utf-8

from honeybee.model import Model
from honeybee.room import Room
import honeybee_energy.lib.programtypes as prog_type_lib

import os
import json


def model_energy_properties_office(directory):
    room = Room.from_box('Closed_Office', 5, 10, 3)
    room.properties.energy.program_type = prog_type_lib.office_program
    room.properties.energy.add_default_ideal_air()

    model = Model('Office_Test_Box', [room])
    model_dict = model.to_dict()

    dest_file = os.path.join(directory, 'model_energy_properties_office.json')
    with open(dest_file, 'w') as fp:
        json.dump(model_dict['properties']['energy'], fp, indent=4)


# run all functions within the file
master_dir = os.path.split(os.path.dirname(__file__))[0]
sample_directory = os.path.join(master_dir, 'samples', 'properties')

model_energy_properties_office(sample_directory)
