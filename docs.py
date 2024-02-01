"""generate openapi docs."""
from pkg_resources import get_distribution
from pydantic_openapi_helper.core import get_openapi
from pydantic_openapi_helper.inheritance import class_mapper
from honeybee_schema.model import Model
from honeybee_schema.energy.simulation import SimulationParameter
from honeybee_schema.validation import ValidationReport
from honeybee_schema.comparison import ComparisonReport, SyncInstructions
from honeybee_schema.projectinfo import ProjectInfo

import json
import argparse

parser = argparse.ArgumentParser(description='Generate OpenAPI JSON schemas')

parser.add_argument('--version', help='Set the version of the new OpenAPI Schema')

args = parser.parse_args()

if args.version:
    VERSION = args.version.replace('v', '')
else:
    VERSION = '.'.join(get_distribution('honeybee_schema').version.split('.')[:3])

info = {
    "description": "",
    "version": VERSION,
    "title": "",
    "contact": {
        "name": "Ladybug Tools",
        "email": "info@ladybug.tools",
        "url": "https://github.com/ladybug-tools/honeybee-schema"
    },
    "x-logo": {
        "url": "https://www.ladybug.tools/assets/img/honeybee-large.png",
        "altText": "Honeybee logo"
    },
    "license": {
        "name": "BSD",
        "url": "https://github.com/ladybug-tools-in2/honeybee-schema/blob/master/LICENSE"
    }
}

modules = [
    {'module': [Model], 'name': 'Model'},
    {'module': [SimulationParameter], 'name': 'Simulation Parameter'},
    {'module': [ValidationReport], 'name': 'Validation Report'},
    {'module': [ComparisonReport], 'name': 'Comparison Report'},
    {'module': [SyncInstructions], 'name': 'Sync Instructions'},
    {'module': [ProjectInfo], 'name': 'Project Information'}
]


def _process_name(name):
    """Process module name."""
    new_name = '-'.join(n.lower() for n in name.split())
    return new_name


for module in modules:
    # generate Recipe open api schema
    print(f'Generating {module["name"]} documentation...')

    external_docs = {
        "description": "OpenAPI Specification with Inheritance",
        "url": f"./{_process_name(module['name'])}_inheritance.json"
    }

    openapi = get_openapi(
        module['module'],
        title=f'Honeybee {module["name"]} Schema',
        description=f'Honeybee {_process_name(module["name"])} schema.',
        version=VERSION, info=info,
        external_docs=external_docs
    )

    # Make Model version read-only
    if module['module'][0] is Model:
        model_object = openapi['components']['schemas']['Model']
        model_object['properties']['version']['readOnly'] = True
        model_object['properties']['version']['default'] = VERSION

    with open(f'./docs/{_process_name(module["name"])}.json', 'w') as out_file:
        json.dump(openapi, out_file, indent=2)

    # with inheritance
    openapi = get_openapi(
        module['module'],
        title=f'Honeybee {module["name"]} Schema',
        description=f'Documentation for Honeybee {_process_name(module["name"])} schema',
        version=VERSION, info=info,
        inheritance=True,
        external_docs=external_docs
    )

    # set the version default key in the Recipe schema
    if module['module'][0] is Model:
        model_object = openapi['components']['schemas']['Model']
        model_object['allOf'][1]['properties']['version']['readOnly'] = True
        model_object['allOf'][1]['properties']['version']['default'] = VERSION

    with open(f'./docs/{_process_name(module["name"])}_inheritance.json', 'w') \
            as out_file:
        json.dump(openapi, out_file, indent=2)

    # add the mapper file
    with open(f'./docs/{_process_name(module["name"])}_mapper.json', 'w') as out_file:
        json.dump(class_mapper(module['module']), out_file, indent=2)

# generate JSONSchema for Honeybee model
with open('./docs/model_json_schema.json', 'w') as out_file:
    out_file.write(Model.schema_json(indent=2))

# generate schema for mode with inheritance but without discriminator
# we will use this file for generating redocly - the full model is too big, and the
# model with inheritance and discriminators is renders incorrectly
external_docs = {
    "description": "OpenAPI Specification with Inheritance",
    "url": "./model_inheritance.json"
}

openapi = get_openapi(
    [Model],
    title='Honeybee Model Schema',
    description='Documentation for Honeybee model schema',
    version=VERSION, info=info,
    inheritance=True,
    external_docs=external_docs,
    add_discriminator=False
)

with open('./docs/model_redoc.json', 'w') as out_file:
    json.dump(openapi, out_file, indent=2)
