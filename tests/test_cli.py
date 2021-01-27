"""Test the CLI updater commands."""
import json
from click.testing import CliRunner

from honeybee_schema.cli import update_model


def test_update_model():
    input_model = './tests/json/model_old.hbjson'
    runner = CliRunner()
    result = runner.invoke(update_model, [input_model])
    assert result.exit_code == 0

    model_dict = json.loads(result.output)

    model_ver = tuple(int(v) for v in model_dict['version'].split('.'))
    assert model_ver >= (1, 40, 1)

    updated_hvac = model_dict['properties']['energy']['hvacs'][0]
    assert updated_hvac['vintage'] == 'ASHRAE_2010'
    assert updated_hvac['equipment_type'] == 'PSZAC_DCW_DHW'
