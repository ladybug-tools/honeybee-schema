from honeybee_schema.energy.constructionset import ConstructionSetAbridged, \
    WallConstructionSetAbridged, RoofCeilingConstructionSetAbridged, FloorConstructionSetAbridged, ApertureConstructionSetAbridged, \
    DoorConstructionSetAbridged, ConstructionSet
import os

# target folder where all of the samples live
root = os.path.dirname(os.path.dirname(__file__))
target_folder = os.path.join(root, 'samples', 'construction_set')


def test_constructionset_abridged_complete():
    file_path = os.path.join(target_folder, 'constructionset_abridged_complete.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        ConstructionSetAbridged.model_validate_json(f.read())


def test_constructionset_abridged_partial_exterior():
    file_path = os.path.join(target_folder, 'constructionset_abridged_partial_exterior.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        ConstructionSetAbridged.model_validate_json(f.read())


def test_constructionset_full_complete():
    file_path = os.path.join(target_folder, 'constructionset_complete.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        ConstructionSet.model_validate_json(f.read())


def test_constructionset_full_partial_exterior():
    file_path = os.path.join(target_folder, 'constructionset_partial_exterior.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        ConstructionSet.model_validate_json(f.read())
