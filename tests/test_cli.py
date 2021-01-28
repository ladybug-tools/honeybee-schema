"""Test the CLI updater commands."""
import json
import pathlib

from click.testing import CliRunner
from honeybee_schema.cli import update_model


def test_update_model():
    input_model = './tests/json/model_old.hbjson'
    output_model = pathlib.Path('./tests/json/model_new.hbjson')
    runner = CliRunner()
    result = runner.invoke(
        update_model, [input_model, '--output-file', output_model.as_posix()]
    )
    assert result.exit_code == 0

    model_dict = json.loads(output_model.read_bytes())

    model_ver = tuple(int(v) for v in model_dict['version'].split('.'))
    assert model_ver >= (1, 40, 1)

    updated_hvac = model_dict['properties']['energy']['hvacs'][0]
    assert updated_hvac['vintage'] == 'ASHRAE_2010'
    assert updated_hvac['equipment_type'] == 'PSZAC_DCW_DHW'

    output_model.unlink()
