import os
import json
import math

from ladybug_geometry.geometry2d.pointvector import Vector2D
from ladybug_geometry.geometry3d import Polyface3D
from ladybug_geometry.geometry3d import Face3D
from honeybee.shade import Shade
from honeybee.aperture import Aperture
from honeybee.room import Room
from honeybee.model import Model
from honeybee_energy.schedule.ruleset import ScheduleRuleset
from honeybee_energy.load.equipment import GasEquipment
import honeybee_energy.lib.programtypes as prog_type_lib
import honeybee_energy.lib.constructionsets as constr_set_lib
from dragonfly.windowparameter import RepeatingWindowRatio, SimpleWindowRatio
from dragonfly.room2d import Room2D
from dragonfly.story import Story
from dragonfly.building import Building


def single_family_home(directory):
    poly_file = './scripts/geometry/single_family_geo.json'
    with open(poly_file, 'r') as fp:
        geo_dict = json.load(fp)

    # create the basic Room objects
    program = prog_type_lib.program_type_by_identifier('2013::MidriseApartment::Apartment')
    c_set = constr_set_lib.construction_set_by_identifier('2013::ClimateZone5::SteelFramed')
    rooms = []
    for i, room_geo_dict in enumerate(geo_dict['rooms']):
        room_geo = Polyface3D.from_dict(room_geo_dict)
        room = Room.from_polyface3d('House_Room_{}'.format(i), room_geo)
        room.properties.energy.program_type = program
        room.properties.energy.construction_set = c_set
        room.properties.energy.add_default_ideal_air()
        rooms.append(room)

    # make some of the rooms different to make it interesting
    program2 = prog_type_lib.program_type_by_identifier('2013::MidriseApartment::Corridor')
    rooms[6].properties.energy.program_type = program2
    cook_vals = [0, 0, 0, 0, 0, 0, 0, 0.5, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 0, 0, 0, 0, 0, 0, 0]
    cook_meals = ScheduleRuleset.from_daily_values('Cooking_Meals', cook_vals)
    kitchen_equip = GasEquipment('Kitchen Stove', 20, cook_meals)
    rooms[0].properties.energy.gas_equipment = kitchen_equip

    # add the apertures to the rooms
    apertures = []
    for i, ap_geo in enumerate(geo_dict['apertures']):
        ap_face = Face3D.from_dict(ap_geo)
        hb_ap = Aperture('House_Aperture_{}'.format(i), ap_face)
        hb_ap.extruded_border(0.3)
        apertures.append(hb_ap)

    # assign apertures and solve adjacency
    for room in rooms:
        for face in room.faces:
            for sf in apertures:
                if face.geometry.is_sub_face(sf.geometry, 0.01, 1.0):
                    face.add_aperture(sf)
    Room.solve_adjacency(rooms, 0.01)

    # load up the context shades
    shades = []
    for i, shd_geo in enumerate(geo_dict['shades']):
        shd_face = Face3D.from_dict(shd_geo)
        shades.append(Shade('Context_Shade_{}'.format(i), shd_face))

    # put it all together in a Model and write out the JSON
    model = Model('Single_Family_Home', rooms=rooms, orphaned_shades=shades,
                  units='Meters', tolerance=0.01, angle_tolerance=1.0)
    dest_file = os.path.join(directory, 'single_family_home.hbjson')
    with open(dest_file, 'w') as fp:
        json.dump(model.to_dict(), fp, indent=4)


def lab_building(directory):
    poly_file = './scripts/geometry/lab_building_geo.json'
    with open(poly_file, 'r') as fp:
        geo_dict = json.load(fp)

    # get all of the programs and construction sets
    c_set = constr_set_lib.construction_set_by_identifier('2013::ClimateZone5::SteelFramed')
    office = prog_type_lib.program_type_by_identifier('2013::MediumOffice::ClosedOffice')
    writeup = prog_type_lib.program_type_by_identifier('2013::Laboratory::Office')
    lab_support = prog_type_lib.program_type_by_identifier('2013::Laboratory::Lab with fume hood')
    laboratory = prog_type_lib.program_type_by_identifier('2013::Laboratory::Open lab')
    conference = prog_type_lib.program_type_by_identifier('2013::MediumOffice::Conference')
    classroom = prog_type_lib.program_type_by_identifier('2013::MediumOffice::Classroom')
    corridor = prog_type_lib.program_type_by_identifier('2013::MediumOffice::Corridor')
    storage = prog_type_lib.program_type_by_identifier('2013::MediumOffice::Storage')
    progs = [office, writeup, lab_support, laboratory, conference, classroom,
             corridor, storage]
    prog_keys = ['office', 'writeup', 'lab_support', 'laboratory', 'conference',
                 'classroom', 'corridor', 'storage']

    # create the basic Room objects
    rooms = []
    for prog_key, program in zip(prog_keys, progs):
        for i, room_geo_dict in enumerate(geo_dict[prog_key]):
            room_geo = Face3D.from_dict(room_geo_dict)
            room = Room2D('{}_{}'.format(prog_key, i), room_geo, 3.5)
            room.properties.energy.program_type = program
            room.properties.energy.construction_set = c_set
            room.properties.energy.add_default_ideal_air()
            rooms.append(room)

    # solve adjacency and set windows + shades
    story = Story('Lab_Floor_1', rooms, 4)
    story.remove_room_2d_colinear_vertices(0.01)
    story.intersect_room_2d_adjacency(0.01)
    story.solve_room_2d_adjacency(0.01)
    story.set_outdoor_window_parameters(RepeatingWindowRatio(0.35, 2.8, 0.8, 3))
    story.set_ground_contact(True)
    story.set_top_exposed(True)
    bldg = Building('Lab_Building', [story])

    # create the honeybee model
    model = bldg.to_honeybee(tolerance=0.01)
    model.units = 'Meters'
    model.tolerance = 0.01
    model.angle_tolerance = 1.0

    # generate louvers for all of the apertures
    for ap in model.apertures:
        ap.louvers_by_count(1, 0.5, 0.0, 0.0, Vector2D(1, 0))

    # write the model to a JSON
    dest_file = os.path.join(directory, 'lab_building.hbjson')
    with open(dest_file, 'w') as fp:
        json.dump(model.to_dict(), fp, indent=4)


def urban_district(directory):
    com_poly_file = './scripts/geometry/urban_commercial_geo.json'
    res_poly_file = './scripts/geometry/urban_residential_geo.json'
    with open(com_poly_file, 'r') as fp:
        com_geo_dict = json.load(fp)
    with open(res_poly_file, 'r') as fp:
        res_geo_dict = json.load(fp)

    # get all of the programs and construction sets
    c_set = constr_set_lib.construction_set_by_identifier('2013::ClimateZone5::SteelFramed')
    office = prog_type_lib.program_type_by_identifier('2013::MediumOffice::ClosedOffice')
    apartment = prog_type_lib.program_type_by_identifier('2013::MidriseApartment::Apartment')
    retail = prog_type_lib.program_type_by_identifier('2013::Retail::Retail')

    # create the Room2Ds
    rooms = []
    for j, bldg in enumerate(com_geo_dict):
        for i, floor in enumerate(bldg):
            room_geo = Face3D.from_dict(floor)
            if i < 3:
                hgt = 5 if i == 0 else 4
            else:
                hgt = 3
            program = retail if i == 0 else office
            room = Room2D('Commercial_{}_Room_{}'.format(j, i), room_geo, hgt)
            room.properties.energy.program_type = program
            room.properties.energy.construction_set = c_set
            room.properties.energy.add_default_ideal_air()
            ratio = 0.8 if i == 0 else 0.4
            room.set_outdoor_window_parameters(SimpleWindowRatio(ratio))
            if i == 0:
                room.is_ground_contact = True
            rooms.append(room)

    for j, bldg in enumerate(res_geo_dict):
        for i, floor in enumerate(bldg):
            room_geo = Face3D.from_dict(floor)
            room = Room2D('Residential_{}_Room_{}'.format(j, i), room_geo, 4)
            room.properties.energy.program_type = apartment
            room.properties.energy.construction_set = c_set
            room.properties.energy.add_default_ideal_air()
            room.set_outdoor_window_parameters(SimpleWindowRatio(0.35))
            if i == 0:
                room.is_ground_contact = True
            rooms.append(room)

    # create honeybee Rooms
    hb_rooms = [room.to_honeybee()[0] for room in rooms]
    model = Model('Mass_Pike_District', rooms=hb_rooms,
                  units='Meters', tolerance=0.01, angle_tolerance=1.0)

    # write the model to a JSON
    dest_file = os.path.join(directory, 'urban_district.hbjson')
    with open(dest_file, 'w') as fp:
        json.dump(model.to_dict(), fp, indent=4)


# run all functions within the file
master_dir = os.path.split(os.path.dirname(__file__))[0]
sample_directory = os.path.join(master_dir, 'samples', 'model_large')

single_family_home(sample_directory)
lab_building(sample_directory)
urban_district(sample_directory)
