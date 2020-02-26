"""generate openapi docs."""
from honeybee_schema._openapi import get_openapi
from honeybee_schema.model import Model
from honeybee_schema.energy.simulation import SimulationParameter

import json
import argparse

parser =  argparse.ArgumentParser(description='Generate OpenAPI JSON schemas')

parser.add_argument('--version',
                    help='Set the version of the new OpenAPI Schema')

args = parser.parse_args()

VERSION = None

if args.version:
    VERSION = args.version.replace('v', '')

# generate Model open api schema
print('Generating Model documentation...')
openapi = get_openapi(
    [Model],
    title='Honeybee Model Schema',
    description='This is the documentation for Honeybee model schema.',
    version=VERSION)
with open('./docs/model.json', 'w') as out_file:
    json.dump(openapi, out_file, indent=2)

# generate SimulationParameter open api schema
print('Generating Energy Simulation Parameter documentation...')
openapi = get_openapi(
    [SimulationParameter],
    title='Honeybee Energy Simulation Parameter Schema',
    description='This is the documentation for Honeybee energy simulation parameter schema.',
    version=VERSION)
with open('./docs/simulation-parameter.json', 'w') as out_file:
    json.dump(openapi, out_file, indent=2)
