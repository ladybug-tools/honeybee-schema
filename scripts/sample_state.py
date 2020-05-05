# coding=utf-8
from __future__ import division

from honeybee_radiance.dynamic import RadianceShadeState, RadianceSubFaceState, \
    StateGeometry
from honeybee_radiance.modifier.material import Plastic, Glass, Trans, BSDF

from honeybee.shade import Shade
from honeybee.aperture import Aperture
from ladybug_geometry.geometry3d.pointvector import Point3D
from ladybug_geometry.geometry3d.face import Face3D

import os
import json


def shade_state_abridged_snow(directory):
    snow_mod = Plastic.from_single_reflectance('SnowMaterial', 0.7)
    snow = RadianceShadeState(snow_mod)

    dest_file = os.path.join(directory, 'shade_state_abridged_snow.json')
    with open(dest_file, 'w') as fp:
        json.dump(snow.to_dict(abridged=True), fp, indent=4)


def shade_state_abridged_tree_foliage(directory):
    shd1 = StateGeometry.from_vertices(
        'tree_foliage1', [[0, 0, 5], [2, 0, 5], [2, 2, 5], [0, 2, 5]])
    shd2 = StateGeometry.from_vertices(
        'tree_foliage2', [[0, 0, 5], [-2, 0, 5], [-2, 2, 5], [0, 2, 5]])
    trans1 = Glass.from_single_transmittance('TreeTrans1', 0.5)
    trans2 = Glass.from_single_transmittance('TreeTrans2', 0.27)
    shd1.modifier = trans1
    shd2.modifier = trans2
    tr4 = RadianceShadeState(shades=[shd1, shd2])

    dest_file = os.path.join(directory, 'shade_state_abridged_tree_foliage.json')
    with open(dest_file, 'w') as fp:
        json.dump(tr4.to_dict(abridged=True), fp, indent=4)


def aperture_state_abridged_electrochromic(directory):
    ecglass4 = Glass.from_single_transmittance('ElectrochromicGlass4', 0.01)
    tint4 = RadianceSubFaceState(ecglass4)

    dest_file = os.path.join(directory, 'aperture_state_abridged_electrochromic.json')
    with open(dest_file, 'w') as fp:
        json.dump(tint4.to_dict(abridged=True), fp, indent=4)


def aperture_state_abridged_shades(directory):
    mod = Trans('DiffusingShade', 0.7, 0.7, 0.7, 0.01, 0, 0.45, 0.01)
    mod_dir = Glass.from_single_transmittance('DiffusingShadeDirect', 0.03)
    mod_shd = Plastic('ShadeMat', 0.65, 0.65, 0.65)
    pts_1 = (Point3D(0, 0, 0), Point3D(2, 0, 0), Point3D(2, 2, 0), Point3D(0, 2, 0))
    pts_2 = (Point3D(0, 0, 2), Point3D(2, 0, 0), Point3D(2, 2, 2), Point3D(0, 2, 2))
    shade1 = StateGeometry('RectangleShade1', Face3D(pts_1))
    shade2 = StateGeometry('RectangleShade2', Face3D(pts_2))
    shade1.modifier = mod_shd
    shade2.modifier = mod_shd
    rad_state = RadianceSubFaceState(mod, [shade1, shade2])
    rad_state.modifier_direct = mod_dir

    dest_file = os.path.join(directory, 'aperture_state_abridged_shades.json')
    with open(dest_file, 'w') as fp:
        json.dump(rad_state.to_dict(abridged=True), fp, indent=4)


def aperture_state_abridged_bsdf(directory):
    relative_path = './scripts/bsdf/klemsfull.xml'
    mod = BSDF(relative_path)
    shd_state = RadianceSubFaceState(mod)

    pts = (Point3D(0, 0, 0), Point3D(0, 0, 3), Point3D(1, 0, 3), Point3D(1, 0, 0))
    ap = Aperture('TestWindow', Face3D(pts))
    ap.properties.radiance.dynamic_group_identifier = 'DynamicShdWindow'
    ap.properties.radiance.states = [shd_state]
    shd_state.gen_geos_from_tmtx_thickness(0.05)

    dest_file = os.path.join(directory, 'aperture_state_abridged_bsdf.json')
    with open(dest_file, 'w') as fp:
        json.dump(shd_state.to_dict(abridged=True), fp, indent=4)


# run all functions within the file
master_dir = os.path.split(os.path.dirname(__file__))[0]
sample_directory = os.path.join(master_dir, 'samples', 'state')

shade_state_abridged_snow(sample_directory)
shade_state_abridged_tree_foliage(sample_directory)
aperture_state_abridged_electrochromic(sample_directory)
aperture_state_abridged_shades(sample_directory)
aperture_state_abridged_bsdf(sample_directory)
