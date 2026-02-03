from honeybee_schema.energy.programtype import ProgramTypeAbridged, ProgramType
import os

# target folder where all of the samples live
root = os.path.dirname(os.path.dirname(__file__))
target_folder = os.path.join(root, 'samples', 'program_type')


def test_program_type_abridged_plenum():
    file_path = os.path.join(target_folder, 'program_type_abridged_plenum.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        ProgramTypeAbridged.model_validate_json(f.read())


def test_program_type_abridged_office():
    file_path = os.path.join(target_folder, 'program_type_abridged_office.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        ProgramTypeAbridged.model_validate_json(f.read())


def test_program_type_abridged_kitchen():
    file_path = os.path.join(target_folder, 'program_type_abridged_kitchen.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        ProgramTypeAbridged.model_validate_json(f.read())


def test_program_type_abridged_patient_room():
    file_path = os.path.join(target_folder, 'program_type_abridged_patient_room.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        ProgramTypeAbridged.model_validate_json(f.read())


def test_program_type_plenum():
    file_path = os.path.join(target_folder, 'program_type_plenum.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        ProgramType.model_validate_json(f.read())


def test_program_type_office():
    file_path = os.path.join(target_folder, 'program_type_office.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        ProgramType.model_validate_json(f.read())
