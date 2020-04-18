"""generate openapi docs."""
from honeybee_schema._openapi import get_openapi
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
    version=VERSION,
    external_docs=external_docs)
with open('./docs/model.json', 'w') as out_file:
    json.dump(openapi, out_file, indent=2)

# with inheritance
openapi = get_openapi(
    [Model],
    title='Honeybee Model Schema',
    description='This is the documentation for Honeybee model schema.',
    version=VERSION,
    inheritance=True,
    external_docs=external_docs
)

with open('./docs/model_inheritance.json', 'w') as out_file:
    json.dump(openapi, out_file, indent=2)

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
    version=VERSION,
    external_docs=external_docs)
with open('./docs/simulation-parameter.json', 'w') as out_file:
    json.dump(openapi, out_file, indent=2)

openapi = get_openapi(
    [SimulationParameter],
    title='Honeybee Energy Simulation Parameter Schema',
    description='This is the documentation for Honeybee energy simulation parameter schema.',
    version=VERSION, inheritance=True,
    external_docs=external_docs
)
with open('./docs/simulation-parameter_inheritance.json', 'w') as out_file:
    json.dump(openapi, out_file, indent=2)
