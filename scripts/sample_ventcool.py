# coding=utf-8
from honeybee_energy.ventcool.opening import VentilationOpening
from honeybee_energy.ventcool.control import VentilationControl
from honeybee_energy.schedule.day import ScheduleDay
from honeybee_energy.schedule.ruleset import ScheduleRuleset
import honeybee_energy.lib.scheduletypelimits as schedule_types

from ladybug.dt import Time

import os
import json


def ventilation_opening_default(directory):
    ventilation = VentilationOpening()
    dest_file = os.path.join(directory, 'ventilation_opening_default.json')
    with open(dest_file, 'w') as fp:
        json.dump(ventilation.to_dict(), fp, indent=4)


def ventilation_control_simple(directory):
    ventilation = VentilationControl(22)

    dest_file = os.path.join(directory, 'ventilation_control_simple.json')
    with open(dest_file, 'w') as fp:
        json.dump(ventilation.to_dict(abridged=True), fp, indent=4)


def ventilation_control_detailed(directory):
    simple_flush = ScheduleDay('Simple Flush', [1, 0, 1],
                               [Time(0, 0), Time(9, 0), Time(22, 0)])
    schedule = ScheduleRuleset('Night Flush Schedule', simple_flush,
                               None, schedule_types.fractional)
    ventilation = VentilationControl(22, 28, 12, 32, 0)
    ventilation.schedule = schedule

    dest_file = os.path.join(directory, 'ventilation_control_detailed.json')
    with open(dest_file, 'w') as fp:
        json.dump(ventilation.to_dict(abridged=True), fp, indent=4)


# run all functions within the file
master_dir = os.path.split(os.path.dirname(__file__))[0]
sample_directory = os.path.join(master_dir, 'samples', 'ventcool')

ventilation_opening_default(sample_directory)
ventilation_control_simple(sample_directory)
ventilation_control_detailed(sample_directory)
