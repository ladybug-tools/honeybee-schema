import pytest
from pydantic import ValidationError

from honeybee_schema.energy.load import People, PeopleAbridged


DEFAULT_CO2_RATE = 3.82e-8
CUSTOM_CO2_RATE = 4e-8


@pytest.mark.parametrize('people_class', (PeopleAbridged, People))
def test_people_carbon_dioxide_generation_rate(people_class):
    people = people_class.model_validate({
        'type': people_class.__name__,
        'identifier': 'Open Office Zone People',
        'people_per_area': 0.05
    })
    assert people.carbon_dioxide_generation_rate == DEFAULT_CO2_RATE

    custom_people = people_class.model_validate({
        'type': people_class.__name__,
        'identifier': 'Open Office Zone People',
        'people_per_area': 0.05,
        'carbon_dioxide_generation_rate': CUSTOM_CO2_RATE
    })
    assert custom_people.carbon_dioxide_generation_rate == CUSTOM_CO2_RATE


@pytest.mark.parametrize('invalid_rate', (-1, None))
def test_people_carbon_dioxide_generation_rate_validation(invalid_rate):
    with pytest.raises(ValidationError):
        PeopleAbridged.model_validate({
            'type': 'PeopleAbridged',
            'identifier': 'Open Office Zone People',
            'people_per_area': 0.05,
            'carbon_dioxide_generation_rate': invalid_rate
        })


def test_people_abridged_honeybee_energy_payload():
    people = PeopleAbridged.model_validate({
        'type': 'PeopleAbridged',
        'identifier': 'Open Office Zone People',
        'people_per_area': 0.05,
        'radiant_fraction': 0.3,
        'latent_fraction': {'type': 'Autocalculate'},
        'carbon_dioxide_generation_rate': CUSTOM_CO2_RATE,
        'occupancy_schedule': 'Always On',
        'activity_schedule': 'Seated Adult Activity'
    })
    assert people.carbon_dioxide_generation_rate == CUSTOM_CO2_RATE


def test_people_carbon_dioxide_generation_rate_schema():
    properties = PeopleAbridged.model_json_schema()['properties']
    co2_schema = properties['carbon_dioxide_generation_rate']

    assert co2_schema['type'] == 'number'
    assert co2_schema['minimum'] == 0
    assert co2_schema['default'] == DEFAULT_CO2_RATE
    assert 'anyOf' not in co2_schema
