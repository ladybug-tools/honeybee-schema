from honeybee_schema.radiance.modifierset import ModifierSetAbridged, ModifierSet

import os

# target folder where all of the samples live
root = os.path.dirname(os.path.dirname(__file__))
target_folder = os.path.join(root, 'samples', 'modifier_set')


def test_modifierset_abridged_complete():
    file_path = os.path.join(target_folder, 'modifierset_abridged_complete.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        ModifierSetAbridged.model_validate_json(f.read())


def test_modifierset_abridged_partial_exterior():
    file_path = os.path.join(target_folder, 'modifierset_abridged_partial_exterior.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        ModifierSetAbridged.model_validate_json(f.read())


def test_modifierset_complete():
    file_path = os.path.join(target_folder, 'modifierset_complete.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        ModifierSet.model_validate_json(f.read())


def test_modifierset_partial_exterior():
    file_path = os.path.join(target_folder, 'modifierset_partial_exterior.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        ModifierSet.model_validate_json(f.read())
