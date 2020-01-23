# coding=utf-8
from __future__ import division

from honeybee_energy.schedule.typelimit import ScheduleTypeLimit
from honeybee_energy.schedule.day import ScheduleDay
from honeybee_energy.schedule.rule import ScheduleRule
from honeybee_energy.schedule.ruleset import ScheduleRuleset
from honeybee_energy.schedule.fixedinterval import ScheduleFixedInterval
import honeybee_energy.lib.scheduletypelimits as schedule_types

from ladybug.dt import Date, Time

import random
import os
import json


def scheduletypelimit_temperature(directory):
    temperature = ScheduleTypeLimit('Temperature', -273.15, None, 'Continuous', 'Temperature')

    dest_file = os.path.join(directory, 'scheduletypelimit_temperature.json')
    with open(dest_file, 'w') as fp:
        json.dump(temperature.to_dict(), fp, indent=4)


def schedule_ruleset_simple_repeating(directory):
    test_vals = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1, 1, 1, 1, 1, 1,
                 0.5, 0.5, 0.5, 0.5, 1, 1, 1, 1, 0.5, 0.5, 0.5, 0.5]
    sched = ScheduleRuleset.from_daily_values('Simple Repeating', test_vals)

    dest_file = os.path.join(directory, 'schedule_ruleset_simple_repeating.json')
    with open(dest_file, 'w') as fp:
        json.dump(sched.to_dict(True), fp, indent=4)


def schedule_primary_school_occupancy(directory):
    weekday_school = ScheduleDay('Weekday School Year', [0, 1, 0.5, 0],
                                 [Time(0, 0), Time(8, 0), Time(15, 0), Time(18, 0)])
    weekend_school = ScheduleDay('Weekend School Year', [0])
    weekday_summer = ScheduleDay('Weekday Summer', [0, 0.5, 0],
                                 [Time(0, 0), Time(9, 0), Time(17, 0)])
    weekend_summer = ScheduleDay('Weekend Summer', [0])

    summer_weekday_rule = ScheduleRule(
        weekday_summer, start_date=Date(7, 1), end_date=Date(9, 1))
    summer_weekday_rule.apply_weekday = True
    summer_weekend_rule = ScheduleRule(
        weekend_summer, start_date=Date(7, 1), end_date=Date(9, 1))
    summer_weekend_rule.apply_weekend = True
    summer_weekend_rule.apply_holiday = True
    school_weekend_rule = ScheduleRule(weekend_school)
    school_weekend_rule.apply_weekend = True
    school_weekend_rule.apply_holiday = True

    summer_design = ScheduleDay('School Summer Design', [0, 1, 0.25],
                                [Time(0, 0), Time(6, 0), Time(18, 0)])
    winter_design = ScheduleDay('School Winter Design', [0])

    schedule = ScheduleRuleset('School Occupancy', weekday_school,
                               [summer_weekday_rule, summer_weekend_rule,
                                school_weekend_rule],
                               schedule_types.fractional, summer_design, winter_design)

    dest_file = os.path.join(directory, 'schedule_primary_school_occupancy.json')
    with open(dest_file, 'w') as fp:
        json.dump(schedule.to_dict(True), fp, indent=4)


def schedule_ruleset_office_occupancy():
    filename = './scripts/standards/OpenStudio_Standards_schedule.json'
    if filename:
        with open(filename, 'r') as f:
            data_store = json.load(f)
    office_sch = ScheduleRuleset.from_standards_dict(data_store['Large Office Bldg Occ'])

    dest_file = os.path.join(directory, 'schedule_ruleset_office_occupancy.json')
    with open(dest_file, 'w') as fp:
        json.dump(office_sch.to_dict(True), fp, indent=4)


def schedule_fixedinterval_increasing_single_day(directory):
    increase_sched = ScheduleFixedInterval(
        'Solstice Increasing', [round(x / 23, 4) for x in range(24)],
        schedule_types.fractional, start_date=Date(6, 21))

    dest_file = os.path.join(
        directory, 'schedule_fixedinterval_increasing_single_day.json')
    with open(dest_file, 'w') as fp:
        json.dump(increase_sched.to_dict(True), fp, indent=4)


def schedule_fixedinterval_increasing_fine_timestep(directory):
    increase_sched = ScheduleFixedInterval(
        'Solstice Increasing', [round(x / 143, 4) for x in range(144)],
        schedule_types.fractional, start_date=Date(6, 21), timestep=6,)

    dest_file = os.path.join(
        directory, 'schedule_fixedinterval_increasing_fine_timestep.json')
    with open(dest_file, 'w') as fp:
        json.dump(increase_sched.to_dict(True), fp, indent=4)


def schedule_fixedinterval_random_annual(directory):
    occ_sched = ScheduleFixedInterval(
        'Random Occupancy', [round(random.random(), 4) for i in range(8760)],
        schedule_types.fractional)

    dest_file = os.path.join(
        directory, 'schedule_fixedinterval_random_annual.json')
    with open(dest_file, 'w') as fp:
        json.dump(occ_sched.to_dict(True), fp, indent=4)


# run all functions within the file
master_dir = os.path.split(os.path.dirname(__file__))[0]
sample_directory = os.path.join(master_dir, 'honeybee_schema', 'samples')

scheduletypelimit_temperature(sample_directory)
schedule_ruleset_simple_repeating(sample_directory)
schedule_primary_school_occupancy(sample_directory)
schedule_fixedinterval_increasing_single_day(sample_directory)
schedule_fixedinterval_increasing_fine_timestep(sample_directory)
schedule_fixedinterval_random_annual(sample_directory)
