"""generate openapi docs."""
from pkg_resources import get_distribution
from honeybee_schema._openapi import get_openapi, class_mapper
from honeybee_schema.model import Model
from honeybee_schema.energy.simulation import SimulationParameter
from honeybee_schema.radiance.asset import SensorGrid, View

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
with open('./docs/model_mapper.json', 'w') as out_file:
    json.dump(class_mapper([Model]), out_file, indent=2)

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
with open('./docs/simulation-parameter_mapper.json', 'w') as out_file:
    json.dump(class_mapper([SimulationParameter]), out_file, indent=2)


# generate Radiance SensorGrid open api schema
print('Generating Radiance SensorGrid documentation...')

external_docs = {
    "description": "OpenAPI Specification with Inheritance",
    "url": "./sensor-grid_inheritance.json"
}

openapi = get_openapi(
    [SensorGrid],
    title='Honeybee Radiance SensorGrid Schema',
    description='This is the documentation for Honeybee SensorGrid schema.',
    version=VERSION, info=info,
    external_docs=external_docs)
with open('./docs/sensor-grid.json', 'w') as out_file:
    json.dump(openapi, out_file, indent=2)

openapi = get_openapi(
    [SensorGrid],
    title='Honeybee Radiance SensorGrid Schema',
    description='This is the documentation for Honeybee SensorGrid schema.',
    version=VERSION, inheritance=True, info=info,
    external_docs=external_docs
)
with open('./docs/sensor-grid_inheritance.json', 'w') as out_file:
    json.dump(openapi, out_file, indent=2)

# add the mapper file
with open('./docs/sensor-grid_mapper.json', 'w') as out_file:
    json.dump(class_mapper([SensorGrid]), out_file, indent=2)


# generate Radiance View open api schema
print('Generating Radiance View documentation...')

external_docs = {
    "description": "OpenAPI Specification with Inheritance",
    "url": "./view_inheritance.json"
}

openapi = get_openapi(
    [View],
    title='Honeybee Radiance View Schema',
    description='This is the documentation for Honeybee View schema.',
    version=VERSION, info=info,
    external_docs=external_docs)
with open('./docs/view.json', 'w') as out_file:
    json.dump(openapi, out_file, indent=2)

openapi = get_openapi(
    [View],
    title='Honeybee Radiance View Schema',
    description='This is the documentation for Honeybee View schema.',
    version=VERSION, inheritance=True, info=info,
    external_docs=external_docs
)
with open('./docs/view_inheritance.json', 'w') as out_file:
    json.dump(openapi, out_file, indent=2)

# add the mapper file
with open('./docs/view_mapper.json', 'w') as out_file:
    json.dump(class_mapper([View]), out_file, indent=2)
