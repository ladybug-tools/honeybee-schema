
from honeybee_schema.model import Model
from pydantic.schema import schema
import pytest 

def test_sort_required_params():
    definitions = schema([Model], ref_prefix='#/components/schemas/')

    schemas = definitions['definitions']
    schema_names = list(schemas.keys())
    schema_names.sort()

    for name in schema_names:
        s = schemas[name]
        if not 'required' in s:
            continue
        properties = s['properties']
        required = s['required']

        sorted_props = {}
        optional = {}
        for prop, value in properties.items():
            if prop in required:
                sorted_props[prop] = value
            else:
                optional[prop] = value

        sorted_props.update(optional)

        if not list(sorted_props.keys())[0:len(required)] == required:
            pytest.fail("Class %s: in this object, not all required parameters are at top of the list"%name)



