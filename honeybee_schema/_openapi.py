from pkg_resources import get_distribution
from pydantic.schema import schema
from typing import Dict

VERSION = None

try:
    VERSION = '.'.join(get_distribution('honeybee_schema').version.split('.')[:3]),
except:
    pass

# base open api dictionary for all schemas
_base_open_api = {
    "openapi": "3.0.2",
    "servers": [],
    "info": {
        "description": "",
        "version": VERSION,
        "title": "",
        "contact": {
            "name": "Ladybug Tools",
            "email": "info@ladybug.tools",
            "url": "https://github.com/ladybug-tools/honeybee-core"
        },
        "x-logo": {
            "url": "https://www.ladybug.tools/assets/img/honeybee-large.png",
            "altText": "Honeybee logo"
        },
        "license": {
            "name": "BSD",
            "url": "https://github.com/ladybug-tools-in2/honeybee-schema/blob/master/LICENSE"
        }
    },
    "externalDocs": {
        "description": "See how to use these schema in action.",
        "url": "https://api.pollination.cloud/"
    },
    "tags": [],
    "x-tagGroups": [
        {
            "name": "Models",
            "tags": []
        }
    ],
    "paths": {},
    "components": {"schemas": {}}
}


def get_openapi(
    base_object,
    title: str = None,
    version: str = None,
    openapi_version: str = "3.0.2",
    description: str = None,
    ) -> Dict:
    """Return Honeybee Model Schema as an openapi compatible dictionary."""
    open_api = dict(_base_open_api)

    open_api['openapi'] = openapi_version

    if title:
        open_api['info']['title'] = title

    if not version and not VERSION:
        raise ValueError('Schema version must be specified as argument or from distribution metadata')

    if version:
        open_api['info']['version'] = version

    if description:
        open_api['info']['description'] = description

    definitions = schema(base_object, ref_prefix='#/components/schemas/')

    # goes to tags
    tags = []
    # goes to x-tagGroups['tags']
    tag_names = []

    schemas = definitions['definitions']
    schema_names = list(schemas.keys())
    schema_names.sort()
    for name in schema_names:
        model_name = '%s_model' % name.lower()
        tag_names.append(model_name)
        tag = {
            'name': model_name,
            'x-displayName': name,
            'description': '<SchemaDefinition schemaRef=\"#/components/schemas/%s\" />\n' % name
        }
        tags.append(tag)

        # sort properties order: put required parameters at begining of the list
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

        s['properties'] = sorted_props

    tag_names.sort()
    open_api['tags'] = tags
    open_api['x-tagGroups'][0]['tags'] = tag_names

    open_api['components']['schemas'] = schemas

    return open_api


if __name__ == '__main__':
    get_openapi()
