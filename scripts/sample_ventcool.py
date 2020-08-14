# coding=utf-8

from honeybee_energy.schedule.day import ScheduleDay
from honeybee_energy.schedule.ruleset import ScheduleRuleset
import honeybee_energy.lib.scheduletypelimits as schedule_types
from honeybee_energy.ventcool.opening import VentilationOpening
from honeybee_energy.ventcool.control import VentilationControl
from honeybee_energy.ventcool.crack import AFNCrack
from honeybee_energy.ventcool.simulation import VentilationSimulationControl

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


def ventilation_crack(directory):
    vent_afn = AFNCrack(flow_coefficient=0.01, flow_exponent=0.65)

    dest_file = os.path.join(directory, 'ventilation_crack.json')
    with open(dest_file, 'w') as fp:
        json.dump(vent_afn.to_dict(), fp, indent=4)


def ventilation_simulation_control(directory):
    vent_sim = VentilationSimulationControl(
        'MultiZoneWithoutDistribution', 21, 101325, 0.5, 'LowRise', 90, 0.5)

    dest_file = os.path.join(directory, 'ventilation_simulation_control.json')
    with open(dest_file, 'w') as fp:
        json.dump(vent_sim.to_dict(), fp, indent=4)


# run all functions within the file
master_dir = os.path.split(os.path.dirname(__file__))[0]
sample_directory = os.path.join(master_dir, 'samples', 'ventcool')

ventilation_opening_default(sample_directory)
ventilation_control_simple(sample_directory)
ventilation_control_detailed(sample_directory)
ventilation_crack(sample_directory)
ventilation_simulation_control(sample_directory)
