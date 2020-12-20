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
from honeybee_energy.material.opaque import EnergyMaterial
from honeybee_energy.schedule.fixedinterval import ScheduleFixedInterval
from honeybee_energy.schedule.ruleset import ScheduleRuleset
from honeybee_energy.schedule.day import ScheduleDay
from honeybee_energy.load.setpoint import Setpoint
from honeybee_energy.load.hotwater import  ServiceHotWater
from honeybee_energy.ventcool.opening import VentilationOpening
from honeybee_energy.ventcool.control import VentilationControl
from honeybee_energy.ventcool import afn
from honeybee_energy.ventcool.simulation import VentilationSimulationControl
from honeybee_energy.hvac.allair.vav import VAV
from honeybee_energy.hvac.doas.fcu import FCUwithDOAS
from honeybee_energy.hvac.heatcool.windowac import WindowAC

import honeybee_energy.lib.programtypes as prog_type_lib
import honeybee_energy.lib.scheduletypelimits as schedule_types
from honeybee_energy.lib.materials import clear_glass, air_gap, roof_membrane, \
    wood, insulation
from honeybee_energy.lib.constructions import generic_exterior_wall, \
    generic_interior_wall, generic_interior_floor, generic_interior_ceiling, \
    generic_double_pane

from honeybee_radiance.modifierset import ModifierSet
from honeybee_radiance.modifier.material import Glass, Plastic, Trans
from honeybee_radiance.dynamic import RadianceShadeState, RadianceSubFaceState, \
    StateGeometry

from ladybug.dt import Time
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

    dest_file = os.path.join(directory, 'model_complete_single_zone_office.hbjson')
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

    dest_file = os.path.join(directory, 'model_complete_user_data.hbjson')
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

    dest_file = os.path.join(directory, 'model_complete_multi_zone_office.hbjson')
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

    dest_file = os.path.join(directory, 'model_complete_patient_room.hbjson')
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

    dest_file = os.path.join(directory, 'model_complete_office_floor.hbjson')
    with open(dest_file, 'w') as fp:
        json.dump(model.to_dict(), fp, indent=4)


def model_complete_holes(directory):
    bound_pts = [Point3D(0, 0), Point3D(9, 0), Point3D(9, 9), Point3D(0, 9)]
    hole_pts = [Point3D(3, 3, 0), Point3D(6, 3, 0), Point3D(6, 6, 0), Point3D(3, 6, 0)]
    face = Face3D(bound_pts, None, [hole_pts])
    polyface = Polyface3D.from_offset_face(face, 3)
    room = Room.from_polyface3d('DonutZone', polyface)

    ap_bound_pts = [Point3D(0.5, 0, 0.5), Point3D(2.5, 0, 0.5), Point3D(2.5, 0, 2.5),
                    Point3D(0.5, 0, 2.5)]
    ap_hole_pts = [Point3D(1, 0, 1), Point3D(2, 0, 1), Point3D(2, 0, 2), Point3D(1, 0, 2)]
    ap_face = Face3D(ap_bound_pts, None, [ap_hole_pts])
    ap = Aperture('HoleAperture', ap_face)
    for face in room.faces:
        if face.geometry.is_sub_face(ap_face, 0.01, 1.0):
            face.add_aperture(ap)

    shd_bound_pts = [Point3D(0, 0, 6), Point3D(9, 0, 6), Point3D(9, 9, 6), Point3D(0, 9, 6)]
    shd_hole_pts1 = [Point3D(2, 2, 6), Point3D(4, 2, 6), Point3D(4, 4, 6), Point3D(2, 4, 6)]
    shd_hole_pts2 = [Point3D(5, 5, 6), Point3D(7, 5, 6), Point3D(7, 7, 6), Point3D(5, 7, 6)]
    s_face = Face3D(shd_bound_pts, None, [shd_hole_pts1, shd_hole_pts2])
    shd = Shade('Canopy', s_face)

    model = Model('Donut_Building', [room], orphaned_shades=[shd])

    dest_file = os.path.join(directory, 'model_complete_holes.hbjson')
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

    dest_file = os.path.join(directory, 'model_energy_shoe_box.hbjson')
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
        directory, 'model_energy_detailed_loads.hbjson')
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

    dest_file = os.path.join(
        directory, 'model_energy_fixed_interval.hbjson')
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

    dest_file = os.path.join(directory, 'model_energy_no_program.hbjson')
    with open(dest_file, 'w') as fp:
        json.dump(model.to_dict(included_prop=['energy']), fp, indent=4)


def model_energy_window_ventilation(directory):
    room = Room.from_box('TinyHouseZone', 5, 10, 3)
    room.properties.energy.add_default_ideal_air()
    south_face = room[3]
    north_face = room[1]
    south_face.apertures_by_ratio(0.4, 0.01)
    north_face.apertures_by_ratio(0.4, 0.01)
    south_face.apertures[0].is_operable = True
    north_face.apertures[0].is_operable = True

    heat_setpt = ScheduleRuleset.from_constant_value(
        'House Heating', 20, schedule_types.temperature)
    cool_setpt = ScheduleRuleset.from_constant_value(
        'House Cooling', 28, schedule_types.temperature)
    setpoint = Setpoint('House Setpoint', heat_setpt, cool_setpt)
    room.properties.energy.setpoint = setpoint

    vent_control = VentilationControl(22, 27, 12, 30)
    room.properties.energy.window_vent_control = vent_control
    ventilation = VentilationOpening(wind_cross_vent=True)
    room.properties.energy.assign_ventilation_opening(ventilation)

    model = Model('TinyHouse', [room])

    dest_file = os.path.join(directory, 'model_energy_window_ventilation.hbjson')
    with open(dest_file, 'w') as fp:
        json.dump(model.to_dict(included_prop=['energy']), fp, indent=4)



def model_energy_service_hot_water(directory):
    room = Room.from_box('TinyHouseZone', 5, 10, 3)
    room.properties.energy.program_type = prog_type_lib.office_program
    simple_office = ScheduleDay('Simple Weekday', [0, 1, 0],
                                [Time(0, 0), Time(9, 0), Time(17, 0)])
    schedule = ScheduleRuleset('Office Water Use', simple_office,
                               None, schedule_types.fractional)
    shw = ServiceHotWater('Office Hot Water', 0.1, schedule)
    room.properties.energy.service_hot_water = shw
    room.properties.energy.add_default_ideal_air()
    model = Model('TinyHouse', [room])

    dest_file = os.path.join(directory, 'model_energy_service_hot_water.hbjson')
    with open(dest_file, 'w') as fp:
        json.dump(model.to_dict(included_prop=['energy']), fp, indent=4)


def model_energy_afn_multizone(directory):
    # south Room
    szone_pts = Face3D(
        [Point3D(0, 0), Point3D(20, 0), Point3D(20, 10), Point3D(0, 10)])
    sroom = Room.from_polyface3d(
        'SouthRoom', Polyface3D.from_offset_face(szone_pts, 3))

    # north Room
    nzone_pts = Face3D(
        [Point3D(0, 10), Point3D(20, 10), Point3D(20, 20), Point3D(0, 20)])
    nroom = Room.from_polyface3d(
        'NorthRoom', Polyface3D.from_offset_face(nzone_pts, 3))

    # add exterior windows on east/west faces
    sroom[2].apertures_by_ratio(0.3)
    nroom[4].apertures_by_ratio(0.3)
    sroom[2].apertures[0].is_operable = True
    nroom[4].apertures[0].is_operable = True

    # add small interior windows on north/south faces
    sroom[3].apertures_by_ratio(0.15)
    nroom[1].apertures_by_ratio(0.15)
    sroom[3].apertures[0].is_operable = True
    nroom[1].apertures[0].is_operable = True

    # ventilation openings
    vent_openings = VentilationOpening(
        fraction_area_operable=1, fraction_height_operable=1, discharge_coefficient=0.6,
        wind_cross_vent=False, flow_coefficient_closed=0.001, flow_exponent_closed=0.667,
        two_way_threshold=0.0001)

    sroom.properties.energy.assign_ventilation_opening(vent_openings)
    nroom.properties.energy.assign_ventilation_opening(vent_openings.duplicate())

    # make ventilation control
    heat_setpt = ScheduleRuleset.from_constant_value(
        'House Heating', 20, schedule_types.temperature)
    cool_setpt = ScheduleRuleset.from_constant_value(
        'House Cooling', 28, schedule_types.temperature)
    setpoint = Setpoint('House Setpoint', heat_setpt, cool_setpt)
    sroom.properties.energy.setpoint = setpoint
    nroom.properties.energy.setpoint = setpoint.duplicate()

    vent_control = VentilationControl(22, 27, 12, 30)
    sroom.properties.energy.window_vent_control = vent_control
    nroom.properties.energy.window_vent_control = vent_control.duplicate()

    # rooms
    rooms = [sroom, nroom]
    for room in rooms:
        # Add program and hvac
        room.properties.energy.program_type = prog_type_lib.office_program

    # make model
    model = Model('Two_Zone_Simple', rooms)
    vsc = VentilationSimulationControl(
        vent_control_type='MultiZoneWithoutDistribution', building_type='LowRise',
        long_axis_angle=0, aspect_ratio=1)
    model.properties.energy.ventilation_simulation_control = vsc

    # make interior faces
    Room.solve_adjacency(rooms, 0.01)

    # make afn
    afn.generate(model.rooms)

    dest_file = os.path.join(directory, 'model_energy_afn.hbjson')
    with open(dest_file, 'w') as fp:
        json.dump(model.to_dict(included_prop=['energy']), fp, indent=4)


def model_energy_allair_hvac(directory):
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

    vav_sys = VAV('VAV System with Glycol Loop')
    vav_sys.vintage = '90.1-2010'
    vav_sys.economizer_type = 'DifferentialDryBulb'
    vav_sys.sensible_heat_recovery = 0.55
    vav_sys.latent_heat_recovery = 0
    first_floor.properties.energy.hvac = vav_sys
    second_floor.properties.energy.hvac = vav_sys

    Room.solve_adjacency([first_floor, second_floor], 0.01)
    model = Model('Model_Energy_Allair_HVAC', [first_floor, second_floor])

    dest_file = os.path.join(directory, 'model_energy_allair_hvac.hbjson')
    with open(dest_file, 'w') as fp:
        json.dump(model.to_dict(included_prop=['energy']), fp, indent=4)


def model_energy_doas_hvac(directory):
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

    fcu_sys = FCUwithDOAS('FCU System with DOAS Enthalpy Wheel')
    fcu_sys.sensible_heat_recovery = 0.81
    fcu_sys.latent_heat_recovery = 0.67
    first_floor.properties.energy.hvac = fcu_sys
    second_floor.properties.energy.hvac = fcu_sys

    Room.solve_adjacency([first_floor, second_floor], 0.01)
    model = Model('Model_Energy_DOAS_HVAC', [first_floor, second_floor])

    dest_file = os.path.join(directory, 'model_energy_doas_hvac.hbjson')
    with open(dest_file, 'w') as fp:
        json.dump(model.to_dict(included_prop=['energy']), fp, indent=4)


def model_energy_window_ac(directory):
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

    ac_sys = WindowAC('FCU System with DOAS Heat Recovery')
    ac_sys.equipment_type = 'Window AC with baseboard gas boiler'
    first_floor.properties.energy.hvac = ac_sys
    second_floor.properties.energy.hvac = ac_sys

    Room.solve_adjacency([first_floor, second_floor], 0.01)
    model = Model('Model_Energy_Window_AC', [first_floor, second_floor])

    dest_file = os.path.join(directory, 'model_energy_window_ac.hbjson')
    with open(dest_file, 'w') as fp:
        json.dump(model.to_dict(included_prop=['energy']), fp, indent=4)


def model_complete_multiroom_radiance(directory):
    triple_pane = Glass.from_single_transmittance('Triple_Pane_0.35', 0.35)
    first_floor = Room.from_box('First_Floor', 10, 10, 3, origin=Point3D(0, 0, 0))
    second_floor = Room.from_box('Second_Floor', 10, 10, 3, origin=Point3D(0, 0, 3))
    for face in first_floor[1:5]:
        face.apertures_by_ratio(0.2, 0.01)
        face.apertures[0].properties.radiance.modifier = triple_pane
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

    mod_set = ModifierSet('Attic_Modifier_Set')
    polyiso = Plastic.from_single_reflectance('PolyIso', 0.45)
    mod_set.roof_ceiling_set.exterior_modifier = polyiso
    attic.properties.radiance.modifier_set = mod_set

    Room.solve_adjacency([first_floor, second_floor, attic], 0.01)

    model = Model('Multi_Room_Radiance_House', [first_floor, second_floor, attic])

    dest_file = os.path.join(directory, 'model_complete_multiroom_radiance.hbjson')
    with open(dest_file, 'w') as fp:
        json.dump(model.to_dict(), fp, indent=4)


def model_radiance_grid_views(directory):
    room = Room.from_box('Tiny_House_Zone', 5, 10, 3)
    garage = Room.from_box('Tiny_Garage', 5, 10, 3, origin=Point3D(5, 0, 0))

    south_face = room[3]
    south_face.apertures_by_ratio(0.4, 0.01)
    south_face.apertures[0].overhang(0.5, indoor=False)
    south_face.apertures[0].overhang(0.5, indoor=True)
    south_face.move_shades(Vector3D(0, 0, -0.5))
    north_face = garage[1]
    north_face.apertures_by_ratio(0.1, 0.01)

    room_grid = room.properties.radiance.generate_sensor_grid(0.5, 0.5, 1)
    garage_grid = garage.properties.radiance.generate_sensor_grid(0.5, 0.5, 1)
    room_view = room.properties.radiance.generate_view((0, -1, 0))
    garage_view = garage.properties.radiance.generate_view((0, 1, 0))

    Room.solve_adjacency([room, garage], 0.01)

    model = Model('Tiny_House', [room, garage])
    model.properties.radiance.sensor_grids = [room_grid]
    model.properties.radiance.add_sensor_grids([garage_grid])
    model.properties.radiance.views = [room_view]
    model.properties.radiance.add_views([garage_view])

    dest_file = os.path.join(directory, 'model_radiance_grid_views.hbjson')
    with open(dest_file, 'w') as fp:
        json.dump(model.to_dict(included_prop=['radiance']), fp, indent=4)


def model_radiance_dynamic_states(directory):
    room = Room.from_box('Tiny_House_Zone', 5, 10, 3)
    garage = Room.from_box('Tiny_Garage', 5, 10, 3, origin=Point3D(5, 0, 0))

    south_face = room[3]
    south_face.apertures_by_ratio(0.5, 0.01)
    shd1 = StateGeometry.from_vertices(
        'outdoor_awning', [[0, 0, 2], [5, 0, 2], [5, 2, 2], [0, 2, 2]])

    ecglass1 = Glass.from_single_transmittance('ElectrochromicState1', 0.4)
    ecglass2 = Glass.from_single_transmittance('ElectrochromicState2', 0.27)
    ecglass3 = Glass.from_single_transmittance('ElectrochromicState3', 0.14)
    ecglass4 = Glass.from_single_transmittance('ElectrochromicState4', 0.01)

    tint1 = RadianceSubFaceState(ecglass1)
    tint2 = RadianceSubFaceState(ecglass2)
    tint3 = RadianceSubFaceState(ecglass3, [shd1])
    tint4 = RadianceSubFaceState(ecglass4, [shd1.duplicate()])
    states = (tint1, tint2, tint3, tint4)
    south_face.apertures[0].properties.radiance.dynamic_group_identifier = \
        'ElectrochromicWindow'
    south_face.apertures[0].properties.radiance.states = states

    shd2 = Shade.from_vertices(
        'indoor_light_shelf', [[0, 0, 2], [-1, 0, 2], [-1, 2, 2], [0, 2, 2]])
    ref_1 = Plastic.from_single_reflectance('outdoor_light_shelf_0.5', 0.5)
    ref_2 = Plastic.from_single_reflectance('indoor_light_shelf_0.70', 0.7)
    light_shelf_1 = RadianceShadeState(ref_1)
    light_shelf_2 = RadianceShadeState(ref_2)
    shelf_states = (light_shelf_1, light_shelf_2)
    shd2.properties.radiance.dynamic_group_identifier = 'DynamicLightShelf'
    shd2.properties.radiance.states = shelf_states
    room.add_indoor_shade(shd2)

    north_face = room[1]
    north_face.overhang(0.25, indoor=False)
    door_verts = [Point3D(2, 10, 0.1), Point3D(1, 10, 0.1),
                  Point3D(1, 10, 2.5), Point3D(2, 10, 2.5)]
    door = Door('Front_Door', Face3D(door_verts))
    north_face.add_door(door)

    aperture_verts = [Point3D(4.5, 10, 1), Point3D(2.5, 10, 1),
                      Point3D(2.5, 10, 2.5), Point3D(4.5, 10, 2.5)]
    aperture = Aperture('Front_Aperture', Face3D(aperture_verts))
    triple_pane = Glass.from_single_transmittance('custom_triple_pane_0.3', 0.3)
    aperture.properties.radiance.modifier = triple_pane
    north_face.add_aperture(aperture)

    tree_canopy_geo = Face3D.from_regular_polygon(
        6, 2, Plane(Vector3D(0, 0, 1), Point3D(5, -3, 4)))
    tree_canopy = Shade('Tree_Canopy', tree_canopy_geo)
    sum_tree_trans = Trans.from_single_reflectance('SummerLeaves', 0.3, 0.0, 0.1, 0.15, 0.15)
    win_tree_trans = Trans.from_single_reflectance('WinterLeaves', 0.1, 0.0, 0.1, 0.1, 0.6)
    summer = RadianceShadeState(sum_tree_trans)
    winter = RadianceShadeState(win_tree_trans)
    tree_canopy.properties.radiance.dynamic_group_identifier = 'DeciduousTree'
    tree_canopy.properties.radiance.states = (summer, winter)

    ground_geo = Face3D.from_rectangle(10, 10, Plane(o=Point3D(0, -10, 0)))
    ground = Shade('Ground', ground_geo)
    grass = Plastic.from_single_reflectance('grass', 0.3)
    snow = Plastic.from_single_reflectance('snow', 0.7)
    summer_ground = RadianceShadeState(grass)
    winter_ground = RadianceShadeState(snow)
    ground.properties.radiance.dynamic_group_identifier = 'SeasonalGround'
    ground.properties.radiance.states = (summer_ground, winter_ground)

    east_face = room[2]
    east_face.apertures_by_ratio(0.1, 0.01)
    west_face = garage[4]
    west_face.apertures_by_ratio(0.1, 0.01)
    Room.solve_adjacency([room, garage], 0.01)

    model = Model('Tiny_House', [room, garage], orphaned_shades=[ground, tree_canopy])

    model_dict = model.to_dict(included_prop=['radiance'])

    dest_file = os.path.join(directory, 'model_radiance_dynamic_states.hbjson')
    with open(dest_file, 'w') as fp:
        json.dump(model_dict, fp, indent=4)


def model_5vertex_sub_faces(directory):
    room = Room.from_box('TinyHouseZone', 5, 10, 3)
    north_face = room[1]
    aperture_verts = [Point3D(4.5, 10, 1), Point3D(2.5, 10, 1), Point3D(2.5, 10, 2.5),
                      Point3D(3.5, 10, 2.9), Point3D(4.5, 10, 2.5)]
    aperture = Aperture('FrontAperture', Face3D(aperture_verts))
    north_face.add_aperture(aperture)
    door_verts = [Point3D(2, 10, 0.1), Point3D(1, 10, 0.1), Point3D(1, 10, 2.5),
                  Point3D(1.5, 10, 2.8), Point3D(2, 10, 2.5)]
    door = Door('FrontDoor', Face3D(door_verts))
    north_face.add_door(door)

    model = Model('TinyHouse', [room])
    model_dict = model.to_dict()

    dest_file = os.path.join(directory, 'model_5vertex_sub_faces.hbjson')
    with open(dest_file, 'w') as fp:
        json.dump(model_dict, fp, indent=4)


def model_5vertex_sub_faces_interior(directory):
    room1 = Room.from_box('TinyHouseZone1', 5, 10, 3)
    north_face = room1[1]
    aperture_verts = [Point3D(4.5, 10, 1), Point3D(2.5, 10, 1), Point3D(2.5, 10, 2.5),
                      Point3D(3.5, 10, 2.9), Point3D(4.5, 10, 2.5)]
    aperture = Aperture('FrontAperture', Face3D(aperture_verts))
    north_face.add_aperture(aperture)
    door_verts = [Point3D(2, 10, 0.1), Point3D(1, 10, 0.1), Point3D(1, 10, 2.5),
                  Point3D(1.5, 10, 2.8), Point3D(2, 10, 2.5)]
    door = Door('FrontDoor', Face3D(door_verts))
    north_face.add_door(door)

    room2 = Room.from_box('TinyHouseZone2', 5, 10, 3, origin=Point3D(0, 10, 0))
    south_face = room2[3]
    s_aperture = Aperture('BackAperture', Face3D(aperture_verts))
    south_face.add_aperture(s_aperture)
    s_door = Door('BackDoor', Face3D(door_verts))
    south_face.add_door(s_door)

    Room.solve_adjacency([room1, room2], 0.01)

    model = Model('TinyHouse', [room1, room2])
    model_dict = model.to_dict()

    dest_file = os.path.join(directory, 'model_5vertex_sub_faces_interior.hbjson')
    with open(dest_file, 'w') as fp:
        json.dump(model_dict, fp, indent=4)


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
model_energy_allair_hvac(sample_directory)
model_energy_doas_hvac(sample_directory)
model_energy_window_ac(sample_directory)
model_energy_window_ventilation(sample_directory)
model_energy_service_hot_water(sample_directory)
model_energy_afn_multizone(sample_directory)
model_5vertex_sub_faces(sample_directory)
model_5vertex_sub_faces_interior(sample_directory)

model_complete_multiroom_radiance(sample_directory)
model_radiance_grid_views(sample_directory)
model_radiance_dynamic_states(sample_directory)
