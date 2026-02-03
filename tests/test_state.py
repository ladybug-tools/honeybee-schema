import os
from honeybee_schema.radiance.state import RadianceSubFaceStateAbridged, \
    RadianceShadeStateAbridged


# target folder where all of the samples live
root = os.path.dirname(os.path.dirname(__file__))
target_folder = os.path.join(root, 'samples', 'state')


def test_aperture_state_abridged_bsdf():
    file_path = os.path.join(target_folder, 'aperture_state_abridged_bsdf.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        RadianceSubFaceStateAbridged.model_validate_json(f.read())


def test_aperture_state_abridged_electrochromic():
    file_path = os.path.join(target_folder, 'aperture_state_abridged_electrochromic.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        RadianceSubFaceStateAbridged.model_validate_json(f.read())


def test_aperture_state_abridged_shades():
    file_path = os.path.join(target_folder, 'aperture_state_abridged_shades.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        RadianceSubFaceStateAbridged.model_validate_json(f.read())


def test_shade_state_abridged_snow():
    file_path = os.path.join(target_folder, 'shade_state_abridged_snow.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        RadianceShadeStateAbridged.model_validate_json(f.read())


def test_shade_state_abridged_tree_foliage():
    file_path = os.path.join(target_folder, 'shade_state_abridged_tree_foliage.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        RadianceShadeStateAbridged.model_validate_json(f.read())
