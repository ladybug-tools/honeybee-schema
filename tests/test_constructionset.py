from honeybee_schema.energy.constructionset import ConstructionSetAbridged, \
    WallSetAbridged, RoofCeilingSetAbridged, FloorSetAbridged, ApertureSetAbridged, \
    DoorSetAbridged
import os

# target folder where all of the samples live
root = os.path.dirname(os.path.dirname(__file__))
target_folder = os.path.join(root, 'honeybee_schema', 'samples')


def test_construction_set():
    file_path = os.path.join(target_folder, 'construction_set.json')
    ConstructionSetAbridged.parse_file(file_path)


def test_wall_set():
    file_path = os.path.join(target_folder, 'wall_set.json')
    WallSetAbridged.parse_file(file_path)


def test_roof_set():
    file_path = os.path.join(target_folder, 'roof_ceiling_set.json')
    RoofCeilingSetAbridged.parse_file(file_path)


def test_floor_set():
    file_path = os.path.join(target_folder, 'floor_set.json')
    FloorSetAbridged.parse_file(file_path)


def test_aperture_set():
    file_path = os.path.join(target_folder, 'aperture_set.json')
    ApertureSetAbridged.parse_file(file_path)


def test_construction_set_1():
    file_path = os.path.join(target_folder, 'construction_set_1.json')
    ConstructionSetAbridged.parse_file(file_path)
