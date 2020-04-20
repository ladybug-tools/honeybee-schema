"""generate openapi docs."""
from pkg_resources import get_distribution
from honeybee_schema._openapi import get_openapi, get_model_mapper
from honeybee_schema.model import Model
from honeybee_schema.energy.simulation import SimulationParameter

import json
import argparse

parser = argparse.ArgumentParser(description='Generate OpenAPI JSON schemas')

parser.add_argument('--version',
                    help='Set the version of the new OpenAPI Schema')

args = parser.parse_args()

VERSION = None

if args.version:
    VERSION = args.version.replace('v', '')
else:
    try:
        VERSION = '.'.join(get_distribution('honeybee_schema').version.split('.')[:3]),
    except:
        pass

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


# generate Model open api schema
print('Generating Model documentation...')

external_docs = {
    "description": "OpenAPI Specification with Inheritance",
    "url": "./model_inheritance.json"
}

openapi = get_openapi(
    [Model],
    title='Honeybee Model Schema',
    description='This is the documentation for Honeybee model schema.',
    version=VERSION, info=info,
    external_docs=external_docs)
with open('./docs/model.json', 'w') as out_file:
    json.dump(openapi, out_file, indent=2)

# with inheritance
openapi = get_openapi(
    [Model],
    title='Honeybee Model Schema',
    description='This is the documentation for Honeybee model schema.',
    version=VERSION, info=info,
    inheritance=True,
    external_docs=external_docs
)

with open('./docs/model_inheritance.json', 'w') as out_file:
    json.dump(openapi, out_file, indent=2)

# add the mapper file
mapper = get_model_mapper(Model)
module_mapper = {k: c.__module__ for k, c in mapper.items()}
with open('./docs/model_mapper.json', 'w') as out_file:
    json.dump(module_mapper, out_file, indent=2)

# generate SimulationParameter open api schema
print('Generating Energy Simulation Parameter documentation...')

external_docs = {
    "description": "OpenAPI Specification with Inheritance",
    "url": "./simulation-parameter_inheritance.json"
}

openapi = get_openapi(
    [SimulationParameter],
    title='Honeybee Energy Simulation Parameter Schema',
    description='This is the documentation for Honeybee energy simulation parameter schema.',
    version=VERSION, info=info,
    external_docs=external_docs)
with open('./docs/simulation-parameter.json', 'w') as out_file:
    json.dump(openapi, out_file, indent=2)

openapi = get_openapi(
    [SimulationParameter],
    title='Honeybee Energy Simulation Parameter Schema',
    description='This is the documentation for Honeybee energy simulation parameter schema.',
    version=VERSION, inheritance=True, info=info,
    external_docs=external_docs
)
with open('./docs/simulation-parameter_inheritance.json', 'w') as out_file:
    json.dump(openapi, out_file, indent=2)

# add the mapper file
mapper = get_model_mapper(SimulationParameter)
module_mapper = {k: c.__module__ for k, c in mapper.items()}
with open('./docs/simulation-parameter_mapper.json', 'w') as out_file:
    json.dump(module_mapper, out_file, indent=2)
