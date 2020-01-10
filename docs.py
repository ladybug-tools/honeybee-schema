"""generate openapi docs."""
from honeybee_schema._openapi import get_openapi
from honeybee_schema.model import Model
from honeybee_schema.energy.simulation import SimulationParameter

import json

# generate Model open api schema
print('Generating Model documentation...')
openapi = get_openapi(
    [Model],
    title='Honeybee Model Schema',
    description='This is the documentation for Honeybee model schema.')
with open('./docs/model.json', 'w') as out_file:
    json.dump(openapi, out_file, indent=2)

# generate SimulationParameter open api schema
print('Generating Energy Simulation Parameter documentation...')
openapi = get_openapi(
    [SimulationParameter],
    title='Honeybee Energy Simulation Parameter Schema',
    description='This is the documentation for Honeybee energy simulation parameter schema.')
with open('./docs/simulation-parameter.json', 'w') as out_file:
    json.dump(openapi, out_file, indent=2)
