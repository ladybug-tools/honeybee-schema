from honeybee_schema.energy.schedule import ScheduleRulesetAbridged, \
    ScheduleFixedIntervalAbridged
import os

# target folder where all of the samples live
root = os.path.dirname(os.path.dirname(__file__))
target_folder = os.path.join(root, 'samples', 'schedule')


def test_ruleset_office_occupancy():
    file_path = os.path.join(
        target_folder, 'schedule_ruleset_office_occupancy.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        ScheduleRulesetAbridged.model_validate_json(f.read())


def test_primary_school_occupancy():
    file_path = os.path.join(
        target_folder, 'schedule_primary_school_occupancy.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        ScheduleRulesetAbridged.model_validate_json(f.read())


def test_ruleset_simple_repeating():
    file_path = os.path.join(
        target_folder, 'schedule_ruleset_simple_repeating.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        ScheduleRulesetAbridged.model_validate_json(f.read())


def test_fixedinterval_increasing_single_day():
    file_path = os.path.join(
        target_folder, 'schedule_fixedinterval_increasing_single_day.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        ScheduleFixedIntervalAbridged.model_validate_json(f.read())


def test_fixedinterval_increasing_fine_timestep():
    file_path = os.path.join(
        target_folder, 'schedule_fixedinterval_increasing_fine_timestep.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        ScheduleFixedIntervalAbridged.model_validate_json(f.read())


def test_fixedinterval_random_annual():
    file_path = os.path.join(
        target_folder, 'schedule_fixedinterval_random_annual.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        ScheduleFixedIntervalAbridged.model_validate_json(f.read())


def test_fixedinterval_leap_year():
    file_path = os.path.join(
        target_folder, 'schedule_fixedinterval_leap_year.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        ScheduleFixedIntervalAbridged.model_validate_json(f.read())
