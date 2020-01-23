
from honeybee_schema.model import Model
from honeybee_schema._openapi import get_openapi

def test_sort_required_params():
    openapi = get_openapi(
    [Model],
    title='Honeybee Model Schema',
    description='This is the documentation for Honeybee model schema.')

    obj = openapi['components']['schemas']['Door']
    props = obj['properties']
    required = obj['required']

    assert list(props.keys())[0:len(required)] == required, 'Not all required parameters are at top of the list'
