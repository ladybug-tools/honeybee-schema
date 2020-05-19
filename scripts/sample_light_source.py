# coding=utf-8
from __future__ import division

from ladybug.wea import Wea

from honeybee_radiance.lightsource.sky import CertainIrradiance, CIE, \
    ClimateBased, SunMatrix, SkyMatrix

import os
import json


def sky_certian_irradiance(directory):
    sky = CertainIrradiance.from_illuminance(10000)
    dest_file = os.path.join(directory, 'sky_certian_irradiance.json')
    with open(dest_file, 'w') as fp:
        json.dump(sky.to_dict(), fp, indent=4)


def sky_cie(directory):
    sky = CIE(38.186734, 270.410387)
    dest_file = os.path.join(directory, 'sky_cie.json')
    with open(dest_file, 'w') as fp:
        json.dump(sky.to_dict(), fp, indent=4)


def sky_climate_based(directory):
    sky = ClimateBased(38.186734, 270.410387, 702, 225)
    dest_file = os.path.join(directory, 'sky_climate_based.json')
    with open(dest_file, 'w') as fp:
        json.dump(sky.to_dict(), fp, indent=4)


def sun_matrix(directory):
    wea = './scripts/wea/denver.wea'
    wea = Wea.from_file(wea)
    sun_mtx = SunMatrix(wea)
    sun_mtx.north = 10
    dest_file = os.path.join(directory, 'sun_matrix.json')
    with open(dest_file, 'w') as fp:
        json.dump(sun_mtx.to_dict(), fp, indent=4)


def sky_matrix(directory):
    wea = './scripts/wea/denver.wea'
    wea = Wea.from_file(wea)
    sky_mtx = SkyMatrix(wea)
    sky_mtx.north = 10
    dest_file = os.path.join(directory, 'sky_matrix.json')
    with open(dest_file, 'w') as fp:
        json.dump(sky_mtx.to_dict(), fp, indent=4)


# run all functions within the file
master_dir = os.path.split(os.path.dirname(__file__))[0]
sample_directory = os.path.join(master_dir, 'samples', 'light_source')

sky_certian_irradiance(sample_directory)
sky_cie(sample_directory)
sky_climate_based(sample_directory)
sun_matrix(sample_directory)
sky_matrix(sample_directory)

