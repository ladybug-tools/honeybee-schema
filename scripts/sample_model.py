# coding=utf-8
from honeybee.model import Model
from honeybee.room import Room
from honeybee.face import Face
from honeybee.shade import Shade
from honeybee.aperture import Aperture
from honeybee.door import Door
from honeybee.boundarycondition import boundary_conditions
from honeybee.facetype import face_types, Floor, RoofCeiling

from honeybee_energy.constructionset import ConstructionSet
from honeybee_energy.construction.opaque import OpaqueConstruction
from honeybee_energy.construction.window import WindowConstruction
from honeybee_energy.construction.shade import ShadeConstruction
from honeybee_energy.construction.air import AirBoundaryConstruction
from honeybee_energy.material.opaque import EnergyMaterial
from honeybee_energy.schedule.fixedinterval import ScheduleFixedInterval

import honeybee_energy.lib.programtypes as prog_type_lib
import honeybee_energy.lib.scheduletypelimits as schedule_types
from honeybee_energy.lib.materials import clear_glass, air_gap, roof_membrane, \
    wood, insulation
from honeybee_energy.lib.constructions import generic_exterior_wall, \
    generic_interior_wall, generic_interior_floor, generic_interior_ceiling, \
    generic_double_pane

from ladybug_geometry.geometry3d.pointvector import Point3D, Vector3D
from ladybug_geometry.geometry3d.plane import Plane
from ladybug_geometry.geometry3d.face import Face3D
from ladybug_geometry.geometry3d.polyface import Polyface3D

import os
import json
import random


def model_complete_single_zone_office(directory):
    room = Room.from_box('Tiny_House_Office', 5, 10, 3)
    room.properties.energy.program_type = prog_type_lib.office_program
    room.properties.energy.add_default_ideal_air()

    stone = EnergyMaterial('Thick Stone', 0.3, 2.31, 2322, 832, 'Rough',
                           0.95, 0.75, 0.8)
    thermal_mass_constr = OpaqueConstruction('Thermal Mass Floor', [stone])
    room[0].properties.energy.construction = thermal_mass_constr

    south_face = room[3]
    south_face.apertures_by_ratio(0.4, 0.01)
    south_face.apertures[0].overhang(0.5, indoor=False)
    south_face.apertures[0].overhang(0.5, indoor=True)
    south_face.move_shades(Vector3D(0, 0, -0.5))
    light_shelf_out = ShadeConstruction('Outdoor_Light_Shelf', 0.5, 0.5)
    light_shelf_in = ShadeConstruction('Indoor_Light_Shelf', 0.7, 0.7)
    south_face.apertures[0].outdoor_shades[0].properties.energy.construction = light_shelf_out
    south_face.apertures[0].indoor_shades[0].properties.energy.construction = light_shelf_in

    north_face = room[1]
    north_face.overhang(0.25, indoor=False)
    door_verts = [Point3D(2, 10, 0.1), Point3D(1, 10, 0.1),
                  Point3D(1, 10, 2.5), Point3D(2, 10, 2.5)]
    door = Door('Front_Door', Face3D(door_verts))
    north_face.add_door(door)

    aperture_verts = [Point3D(4.5, 10, 1), Point3D(2.5, 10, 1),
                      Point3D(2.5, 10, 2.5), Point3D(4.5, 10, 2.5)]
    aperture = Aperture('Front_Aperture', Face3D(aperture_verts))
    triple_pane = WindowConstruction(
        'Triple Pane Window', [clear_glass, air_gap, clear_glass, air_gap, clear_glass])
    aperture.properties.energy.construction = triple_pane
    north_face.add_aperture(aperture)

    tree_canopy_geo = Face3D.from_regular_polygon(
        6, 2, Plane(Vector3D(0, 0, 1), Point3D(5, -3, 4)))
    tree_canopy = Shade('Tree_Canopy', tree_canopy_geo)

    table_geo = Face3D.from_rectangle(2, 2, Plane(o=Point3D(1.5, 4, 1)))
    table = Shade('Table', table_geo)
    room.add_indoor_shade(table)

    model = Model('Tiny_House', [room], orphaned_shades=[tree_canopy])
    model.north_angle = 15

    model_dict = model.to_dict()

    dest_file = os.path.join(directory, 'model_complete_single_zone_office.json')
    with open(dest_file, 'w') as fp:
        json.dump(model.to_dict(), fp, indent=4)


def model_complete_single_zone_office_user_data(directory):
    room = Room.from_box('Tiny_House_Office', 5, 10, 3)
    room.properties.energy.program_type = prog_type_lib.office_program
    room.properties.energy.add_default_ideal_air()

    south_face = room[3]
    south_face.apertures_by_ratio(0.4, 0.01)
    south_face.apertures[0].overhang(0.5, indoor=False)
    south_face.apertures[0].overhang(0.5, indoor=True)
    south_face.move_shades(Vector3D(0, 0, -0.5))
    light_shelf_out = ShadeConstruction('Outdoor_Light_Shelf', 0.5, 0.5)
    light_shelf_in = ShadeConstruction('Indoor_Light_Shelf', 0.7, 0.7)
    south_face.apertures[0].outdoor_shades[0].properties.energy.construction = light_shelf_out
    south_face.apertures[0].indoor_shades[0].properties.energy.construction = light_shelf_in

    north_face = room[1]
    north_face.overhang(0.25, indoor=False)
    door_verts = [Point3D(2, 10, 0.1), Point3D(1, 10, 0.1),
                  Point3D(1, 10, 2.5), Point3D(2, 10, 2.5)]
    door = Door('Front_Door', Face3D(door_verts))
    north_face.add_door(door)

    aperture_verts = [Point3D(4.5, 10, 1), Point3D(2.5, 10, 1),
                      Point3D(2.5, 10, 2.5), Point3D(4.5, 10, 2.5)]
    aperture = Aperture('Front_Aperture', Face3D(aperture_verts))
    north_face.add_aperture(aperture)
    
    model = Model('Tiny_House', [room])
    model_dict = model.to_dict()

    model_dict['user_data'] = {'site': 'The backyard'}
    model_dict['rooms'][0]['user_data'] = {'alt_name': 'Little old tiny house'}
    model_dict['rooms'][0]['faces'][0]['user_data'] = {'alt_name': 'The floor'}
    model_dict['rooms'][0]['faces'][3]['apertures'][0]['user_data'] = \
        {'alt_name': 'Picture window'}
    model_dict['rooms'][0]['faces'][1]['doors'][0]['user_data'] = \
        {'alt_name': 'Front door'}
    model_dict['rooms'][0]['faces'][3]['apertures'][0]['outdoor_shades'][0]['user_data'] = \
        {'alt_name': 'Awning'}

    dest_file = os.path.join(directory, 'model_complete_user_data.json')
    with open(dest_file, 'w') as fp:
        json.dump(model.to_dict(), fp, indent=4)


def model_complete_multi_zone_office(directory):
    first_floor = Room.from_box('First_Floor', 10, 10, 3, origin=Point3D(0, 0, 0))
    second_floor = Room.from_box('Second_Floor', 10, 10, 3, origin=Point3D(0, 0, 3))
    first_floor.properties.energy.program_type = prog_type_lib.office_program
    second_floor.properties.energy.program_type = prog_type_lib.office_program
    first_floor.properties.energy.add_default_ideal_air()
    second_floor.properties.energy.add_default_ideal_air()
    for face in first_floor[1:5]:
        face.apertures_by_ratio(0.2, 0.01)
    for face in second_floor[1:5]:
        face.apertures_by_ratio(0.2, 0.01)

    pts_1 = [Point3D(0, 0, 6), Point3D(0, 10, 6), Point3D(10, 10, 6), Point3D(10, 0, 6)]
    pts_2 = [Point3D(0, 0, 6), Point3D(5, 0, 9), Point3D(5, 10, 9), Point3D(0, 10, 6)]
    pts_3 = [Point3D(10, 0, 6), Point3D(10, 10, 6), Point3D(5, 10, 9), Point3D(5, 0, 9)]
    pts_4 = [Point3D(0, 0, 6), Point3D(10, 0, 6), Point3D(5, 0, 9)]
    pts_5 = [Point3D(10, 10, 6), Point3D(0, 10, 6), Point3D(5, 10, 9)]
    face_1 = Face('AtticFace1', Face3D(pts_1))
    face_2 = Face('AtticFace2', Face3D(pts_2))
    face_3 = Face('AtticFace3', Face3D(pts_3))
    face_4 = Face('AtticFace4', Face3D(pts_4))
    face_5 = Face('AtticFace5', Face3D(pts_5))
    attic = Room('Attic', [face_1, face_2, face_3, face_4, face_5], 0.01, 1)

    constr_set = ConstructionSet('Attic Construction Set')
    polyiso = EnergyMaterial('PolyIso', 0.2, 0.03, 43, 1210, 'MediumRough')
    roof_constr = OpaqueConstruction('Attic Roof Construction',
                                     [roof_membrane, polyiso, wood])
    floor_constr = OpaqueConstruction('Attic Floor Construction',
                                      [wood, insulation, wood])
    constr_set.floor_set.interior_construction = floor_constr
    constr_set.roof_ceiling_set.exterior_construction = roof_constr
    attic.properties.energy.construction_set = constr_set

    Room.solve_adjacency([first_floor, second_floor, attic], 0.01)

    model = Model('Multi_Zone_Single_Family_House', [first_floor, second_floor, attic])

    dest_file = os.path.join(directory, 'model_complete_multi_zone_office.json')
    with open(dest_file, 'w') as fp:
        json.dump(model.to_dict(), fp, indent=4)


def model_complete_patient_room(directory):
    pat_room_program = \
        prog_type_lib.program_type_by_identifier('2013::Hospital::ICU_PatRm')
    room = Room.from_box('Hospital_Patient_Room', 5, 10, 3)
    room.properties.energy.program_type = pat_room_program

    room.properties.energy.add_default_ideal_air()
    ideal_air = room.properties.energy.hvac.duplicate()
    ideal_air.economizer_type = 'DifferentialEnthalpy'
    ideal_air.sensible_heat_recovery = 0.81
    ideal_air.latent_heat_recovery = 0.68
    room.properties.energy.hvac = ideal_air

    pat_rm_setpoint = room.properties.energy.setpoint.duplicate()
    pat_rm_setpoint.identifier = 'Humidity Controlled PatRm Setpt'
    pat_rm_setpoint.heating_setpoint = 21
    pat_rm_setpoint.cooling_setpoint = 24
    pat_rm_setpoint.humidifying_setpoint = 30
    pat_rm_setpoint.dehumidifying_setpoint = 55
    room.properties.energy.setpoint = pat_rm_setpoint

    south_face = room[3]
    south_face.apertures_by_ratio(0.4, 0.01)
    south_face.apertures[0].overhang(0.5, indoor=False)
    south_face.move_shades(Vector3D(0, 0, -0.5))

    room[0].boundary_condition = boundary_conditions.adiabatic
    room[1].boundary_condition = boundary_conditions.adiabatic
    room[2].boundary_condition = boundary_conditions.adiabatic
    room[4].boundary_condition = boundary_conditions.adiabatic
    room[5].boundary_condition = boundary_conditions.adiabatic

    model = Model('Patient_Room_Test_Box', [room])

    dest_file = os.path.join(directory, 'model_complete_patient_room.json')
    with open(dest_file, 'w') as fp:
        json.dump(model.to_dict(), fp, indent=4)


def model_complete_office_floor(directory):
    pts_1 = [Point3D(0, 0), Point3D(30, 0), Point3D(20, 10), Point3D(10, 10)]
    pts_2 = [Point3D(0, 0), Point3D(10, 10), Point3D(10, 20), Point3D(0, 30)]
    pts_3 = [Point3D(10, 20), Point3D(20, 20), Point3D(30, 30), Point3D(0, 30)]
    pts_4 = [Point3D(30, 0), Point3D(30, 30), Point3D(20, 20), Point3D(20, 10)]
    verts = [pts_1, pts_2, pts_3, pts_4]
    rooms = []
    for i, f_vert in enumerate(verts):
        pface = Polyface3D.from_offset_face(Face3D(f_vert), 3)
        room = Room.from_polyface3d('PerimeterRoom{}'.format(i), pface)
        room.properties.energy.program_type = prog_type_lib.office_program
        room.properties.energy.add_default_ideal_air()
        rooms.append(room)
    rooms.append(Room.from_box('CoreRoom', 10, 10, 3, origin=Point3D(10, 10)))
    adj_info = Room.solve_adjacency(rooms, 0.01)
    for face_pair in adj_info['adjacent_faces']:
        face_pair[0].type = face_types.air_boundary
        face_pair[1].type = face_types.air_boundary
    for room in rooms:
        for face in room:
            if isinstance(face.type, (Floor, RoofCeiling)):
                face.boundary_condition = boundary_conditions.adiabatic

    model = Model('Core_Perimeter_Office_Floor', rooms)

    dest_file = os.path.join(directory, 'model_complete_office_floor.json')
    with open(dest_file, 'w') as fp:
        json.dump(model.to_dict(), fp, indent=4)


def model_energy_shoe_box(directory):
    room = Room.from_box('Simple_Shoe_Box_Zone', 5, 10, 3)
    room[0].boundary_condition = boundary_conditions.adiabatic
    for face in room[2:]:
        face.boundary_condition = boundary_conditions.adiabatic

    north_face = room[1]
    north_face.apertures_by_ratio_rectangle(0.4, 2, 0.7, 2, 0, 0.01)

    constr_set = ConstructionSet('Shoe Box Construction Set')
    constr_set.wall_set.exterior_construction = generic_exterior_wall
    constr_set.wall_set.interior_construction = generic_interior_wall
    constr_set.floor_set.interior_construction = generic_interior_floor
    constr_set.roof_ceiling_set.interior_construction = generic_interior_ceiling
    constr_set.aperture_set.window_construction = generic_double_pane
    room.properties.energy.construction_set = constr_set

    model = Model('Shoe_Box', [room])

    dest_file = os.path.join(directory, 'model_energy_shoe_box.json')
    with open(dest_file, 'w') as fp:
        json.dump(model.to_dict(included_prop=['energy']), fp, indent=4)


def model_energy_detailed_loads(directory):
    room = Room.from_box('Office_Test_Box', 5, 10, 3)
    room.properties.energy.program_type = prog_type_lib.plenum_program
    room.properties.energy.add_default_ideal_air()

    room.properties.energy.people = prog_type_lib.office_program.people
    room.properties.energy.lighting = prog_type_lib.office_program.lighting
    room.properties.energy.electric_equipment = prog_type_lib.office_program.electric_equipment
    room.properties.energy.infiltration = prog_type_lib.office_program.infiltration
    room.properties.energy.ventilation = prog_type_lib.office_program.ventilation
    room.properties.energy.setpoint = prog_type_lib.office_program.setpoint

    room[0].boundary_condition = boundary_conditions.adiabatic
    room[1].boundary_condition = boundary_conditions.adiabatic
    room[2].boundary_condition = boundary_conditions.adiabatic
    room[4].boundary_condition = boundary_conditions.adiabatic
    room[5].boundary_condition = boundary_conditions.adiabatic

    model = Model('Office_Model', [room])

    dest_file = os.path.join(
        directory, 'model_energy_detailed_loads.json')
    with open(dest_file, 'w') as fp:
        json.dump(model.to_dict(included_prop=['energy']), fp, indent=4)


def model_energy_fixed_interval(directory):
    room = Room.from_box('Tiny_House_Office', 5, 10, 3)
    room.properties.energy.program_type = prog_type_lib.office_program
    room.properties.energy.add_default_ideal_air()

    occ_sched = ScheduleFixedInterval(
        'Random Occupancy', [round(random.random(), 4) for i in range(8760)],
        schedule_types.fractional)
    new_people = room.properties.energy.people.duplicate()
    new_people.occupancy_schedule = occ_sched
    room.properties.energy.people = new_people

    south_face = room[3]
    south_face.apertures_by_ratio(0.4, 0.01)
    south_face.apertures[0].overhang(0.5, indoor=False)
    south_face.apertures[0].overhang(0.5, indoor=True)
    south_face.move_shades(Vector3D(0, 0, -0.5))
    light_shelf_out = ShadeConstruction('Outdoor_Light_Shelf', 0.5, 0.5)
    light_shelf_in = ShadeConstruction('Indoor_Light_Shelf', 0.7, 0.7)
    south_face.apertures[0].outdoor_shades[0].properties.energy.construction = light_shelf_out
    south_face.apertures[0].indoor_shades[0].properties.energy.construction = light_shelf_in

    north_face = room[1]
    north_face.overhang(0.25, indoor=False)
    door_verts = [Point3D(2, 10, 0.1), Point3D(1, 10, 0.1),
                  Point3D(1, 10, 2.5), Point3D(2, 10, 2.5)]
    door = Door('Front_Door', Face3D(door_verts))
    north_face.add_door(door)

    aperture_verts = [Point3D(4.5, 10, 1), Point3D(2.5, 10, 1),
                      Point3D(2.5, 10, 2.5), Point3D(4.5, 10, 2.5)]
    aperture = Aperture('Front_Aperture', Face3D(aperture_verts))
    north_face.add_aperture(aperture)

    tree_canopy_geo = Face3D.from_regular_polygon(
        6, 2, Plane(Vector3D(0, 0, 1), Point3D(5, -3, 4)))
    tree_canopy = Shade('Tree_Canopy', tree_canopy_geo)
    winter = [0.75] * 2190
    spring = [0.75 - ((x / 2190) * 0.5) for x in range(2190)]
    summer = [0.25] * 2190
    fall = [0.25 + ((x / 2190) * 0.5) for x in range(2190)]
    trans_sched = ScheduleFixedInterval(
        'Seasonal Tree Transmittance', winter + spring + summer + fall,
        schedule_types.fractional)
    tree_canopy.properties.energy.transmittance_schedule = trans_sched

    model = Model('Tiny_House', [room], orphaned_shades=[tree_canopy])
    model.north_angle = 15

    dest_file = os.path.join(
        directory, 'model_energy_fixed_interval.json')
    with open(dest_file, 'w') as fp:
        json.dump(model.to_dict(included_prop=['energy']), fp, indent=4)
    

def model_energy_no_program(directory):
    room = Room.from_box('Abandoned_Tiny_House', 5, 10, 3)

    stone = EnergyMaterial('Thick Stone', 0.3, 2.31, 2322, 832, 'Rough',
                           0.95, 0.75, 0.8)
    thermal_mass_constr = OpaqueConstruction('Thermal Mass Floor', [stone])
    room[0].properties.energy.construction = thermal_mass_constr

    south_face = room[3]
    south_face.apertures_by_ratio(0.4, 0.01)
    south_face.apertures[0].overhang(0.5, indoor=False)
    south_face.apertures[0].overhang(0.5, indoor=True)
    south_face.move_shades(Vector3D(0, 0, -0.5))
    light_shelf_out = ShadeConstruction('Outdoor_Light_Shelf', 0.5, 0.5)
    light_shelf_in = ShadeConstruction('Indoor_Light_Shelf', 0.7, 0.7)
    south_face.apertures[0].outdoor_shades[0].properties.energy.construction = light_shelf_out
    south_face.apertures[0].indoor_shades[0].properties.energy.construction = light_shelf_in

    north_face = room[1]
    north_face.overhang(0.25, indoor=False)
    door_verts = [Point3D(2, 10, 0.1), Point3D(1, 10, 0.1),
                  Point3D(1, 10, 2.5), Point3D(2, 10, 2.5)]
    door = Door('Front_Door', Face3D(door_verts))
    north_face.add_door(door)

    aperture_verts = [Point3D(4.5, 10, 1), Point3D(2.5, 10, 1),
                      Point3D(2.5, 10, 2.5), Point3D(4.5, 10, 2.5)]
    aperture = Aperture('Front_Aperture', Face3D(aperture_verts))
    triple_pane = WindowConstruction(
        'Triple Pane Window', [clear_glass, air_gap, clear_glass, air_gap, clear_glass])
    aperture.properties.energy.construction = triple_pane
    north_face.add_aperture(aperture)

    tree_canopy_geo = Face3D.from_regular_polygon(
        6, 2, Plane(Vector3D(0, 0, 1), Point3D(5, -3, 4)))
    tree_canopy = Shade('Tree_Canopy', tree_canopy_geo)

    table_geo = Face3D.from_rectangle(2, 2, Plane(o=Point3D(1.5, 4, 1)))
    table = Shade('Table', table_geo)
    room.add_indoor_shade(table)

    model = Model('Tiny_House', [room], orphaned_shades=[tree_canopy])
    model.north_angle = 15

    dest_file = os.path.join(directory, 'model_energy_no_program.json')
    with open(dest_file, 'w') as fp:
        json.dump(model.to_dict(included_prop=['energy']), fp, indent=4)


def model_energy_properties_office(directory):
    room = Room.from_box('Closed_Office', 5, 10, 3)
    room.properties.energy.program_type = prog_type_lib.office_program
    room.properties.energy.add_default_ideal_air()

    model = Model('Office_Test_Box', [room])
    model_dict = model.to_dict()

    dest_file = os.path.join(directory, 'model_energy_properties_office.json')
    with open(dest_file, 'w') as fp:
        json.dump(model_dict['properties']['energy'], fp, indent=4)


# run all functions within the file
master_dir = os.path.split(os.path.dirname(__file__))[0]
sample_directory = os.path.join(master_dir, 'samples', 'model')

model_complete_single_zone_office(sample_directory)
model_complete_single_zone_office_user_data(sample_directory)
model_complete_multi_zone_office(sample_directory)
model_complete_patient_room(sample_directory)
model_complete_office_floor(sample_directory)

model_energy_shoe_box(sample_directory)
model_energy_detailed_loads(sample_directory)
model_energy_fixed_interval(sample_directory)
model_energy_no_program(sample_directory)
model_energy_properties_office(sample_directory)
