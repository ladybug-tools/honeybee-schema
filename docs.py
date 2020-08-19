"""generate openapi docs."""
from pkg_resources import get_distribution
from honeybee_schema._openapi import get_openapi, class_mapper
from honeybee_schema.model import Model
from honeybee_schema.energy.simulation import SimulationParameter
from honeybee_schema.radiance.lightsource import CertainIrradiance, CIE, \
    ClimateBased, SunMatrix, SkyMatrix

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
# set the version default key in the Model schema
openapi['components']['schemas']['Model']['properties']['version']['default'] = VERSION
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
# set the version default key in the Model schema
openapi['components']['schemas']['Model']['allOf'][1]['properties']['version']['default'] = VERSION
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


# generate Radiance Asset open api schema
print('Generating Radiance Asset documentation...')

external_docs = {
    "description": "OpenAPI Specification with Inheritance",
    "url": "./radiance-asset_inheritance.json"
}

openapi = get_openapi(
    [CertainIrradiance, CIE, ClimateBased, SunMatrix, SkyMatrix],
    title='Honeybee Radiance Asset Schema',
    description='This is the documentation for Honeybee Radiance Asset schema.',
    version=VERSION, info=info,
    external_docs=external_docs)
with open('./docs/radiance-asset.json', 'w') as out_file:
    json.dump(openapi, out_file, indent=2)

openapi = get_openapi(
    [CertainIrradiance, CIE, ClimateBased, SunMatrix, SkyMatrix],
    title='Honeybee Radiance Asset Schema',
    description='This is the documentation for Honeybee Radiance Asset Schema.',
    version=VERSION, inheritance=True, info=info,
    external_docs=external_docs
)
with open('./docs/radiance-asset_inheritance.json', 'w') as out_file:
    json.dump(openapi, out_file, indent=2)

# add the mapper file
with open('./docs/radiance-asset_mapper.json', 'w') as out_file:
    json.dump(class_mapper([CertainIrradiance, CIE, ClimateBased,
                            SunMatrix, SkyMatrix]), out_file, indent=2)
