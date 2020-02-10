# coding=utf-8
from honeybee_energy.hvac.idealair import IdealAirSystem
from honeybee_energy.schedule.day import ScheduleDay
from honeybee_energy.schedule.ruleset import ScheduleRuleset
import honeybee_energy.lib.scheduletypelimits as schedule_types

from ladybug.dt import Time

import os
import json


def ideal_air_default(directory):
    ideal_air = IdealAirSystem('Default HVAC System')
    dest_file = os.path.join(directory, 'ideal_air_default.json')
    with open(dest_file, 'w') as fp:
        json.dump(ideal_air.to_dict(abridged=True), fp, indent=4)


def ideal_air_detailed(directory):
    ideal_air = IdealAirSystem('Passive House HVAC System')
    
    ideal_air.economizer_type = 'DifferentialEnthalpy'
    ideal_air.demand_controlled_ventilation = True
    ideal_air.sensible_heat_recovery = 0.75
    ideal_air.latent_heat_recovery = 0.6
    ideal_air.heating_air_temperature = 40
    ideal_air.cooling_air_temperature = 15
    ideal_air.heating_limit = 2000
    ideal_air.cooling_limit = 3500
    sch_day = ScheduleDay('Day Control', [0, 1, 0], [Time(0, 0), Time(8, 0), Time(22, 0)])
    schedule = ScheduleRuleset('HVAC Control', sch_day, None, schedule_types.on_off)
    ideal_air.heating_availability = schedule
    ideal_air.cooling_availability = schedule

    dest_file = os.path.join(directory, 'ideal_air_detailed.json')
    with open(dest_file, 'w') as fp:
        json.dump(ideal_air.to_dict(abridged=True), fp, indent=4)


# run all functions within the file
master_dir = os.path.split(os.path.dirname(__file__))[0]
sample_directory = os.path.join(master_dir, 'samples', 'hvac')

ideal_air_default(sample_directory)
ideal_air_detailed(sample_directory)

