from honeybee_schema.radiance.lightsource import CertainIrradiance, CIE, \
    ClimateBased, SunMatrix, SkyMatrix

import pytest
import os

# target folder where all of the samples live
root = os.path.dirname(os.path.dirname(__file__))
target_folder = os.path.join(root, 'samples', 'light_source')


def test_sky_certian_irradiance():
    file_path = os.path.join(target_folder, 'sky_certian_irradiance.json')
    CertainIrradiance.parse_file(file_path)


def test_sky_cie():
    file_path = os.path.join(target_folder, 'sky_cie.json')
    CIE.parse_file(file_path)


def test_sky_climate_based():
    file_path = os.path.join(target_folder, 'sky_climate_based.json')
    ClimateBased.parse_file(file_path)


def test_sky_matrix():
    file_path = os.path.join(target_folder, 'sky_matrix.json')
    SkyMatrix.parse_file(file_path)


def test_sun_matrix():
    file_path = os.path.join(target_folder, 'sun_matrix.json')
    SunMatrix.parse_file(file_path)
