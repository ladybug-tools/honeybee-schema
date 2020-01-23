
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

        if 'required' in s:
            props = s['properties']
            required = s['required']

            propKeys = props.keys()

            sortedProps = {}
            optional = {}
            for r in propKeys:
                if r in required:
                    sortedProps[r] = props[r]
                else:
                    optional[r] = props[r]

            sortedProps.update(optional)

            s['properties'] = sortedProps

    return schemas


