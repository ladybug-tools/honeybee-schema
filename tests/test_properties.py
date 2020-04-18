from honeybee_schema.radiance.properties import ApertureRadiancePropertiesAbridged, \
    DoorRadiancePropertiesAbridged, FaceRadiancePropertiesAbridged, \
    ShadeRadiancePropertiesAbridged, RoomRadiancePropertiesAbridged, \
    ModelRadianceProperties

import os
import json

# target folder where all of the samples live
root = os.path.dirname(os.path.dirname(__file__))
target_folder = os.path.join(root, 'samples', 'model')


file_path = os.path.join(target_folder, 'model_complete_office_floor.json')
with open(file_path) as json_file:
    office_model = json.load(json_file)


def test_model_radiance_properties():
    model_rad_props = office_model['properties']['radiance']
    ModelRadianceProperties.parse_obj(model_rad_props)


def test_room_radiance_properties():
    room_prop_abridged = office_model['rooms'][0]['properties']['radiance']
    RoomRadiancePropertiesAbridged.parse_obj(room_prop_abridged)


def test_face_radiance_properties():
    face_prop_abridged = office_model['rooms'][0]['faces'][0]['properties']['radiance']
    FaceRadiancePropertiesAbridged.parse_obj(face_prop_abridged)
