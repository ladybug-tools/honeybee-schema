from pkg_resources import get_distribution
from pydantic.utils import get_model
from pydantic.schema import schema, get_flat_models_from_model, get_model_name_map
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
    },
    "externalDocs": {},
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
    external_docs: dict = None,
    inheritance: bool = False
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

    if external_docs:
        open_api['externalDocs'] = external_docs

    if not inheritance:
        schemas = schema(base_object, ref_prefix='#/components/schemas/')['definitions']
    else:
        schemas = get_schemas_inheritance(base_object)

    # goes to tags
    tags = []
    # goes to x-tagGroups['tags']
    tag_names = []

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

        if 'properties' in s:
            properties = s['properties']
        else:
            properties = s['allOf'][1]['properties']

        # make all types readOnly
        try:
            properties['type']['readOnly'] = True
        except KeyError:
            # no type has been set in properties for this object
            typ = {
                'title': 'Type', 'default': f'{name}', 'type': 'string',
                'pattern': f'^{name}$', 'readOnly': True,
            }
            properties['type'] = typ
        # add format to numbers and integers
        # this is helpful for C# generators
        for prop, value in properties.items():
            try:
                if value['type'] == 'number' and 'format' not in value:
                    properties[prop]['format'] = 'double'
                elif value['type'] == 'integer' and 'format' not in value:
                    properties[prop]['format'] = 'int32'
            except KeyError:
                # referenced object
                continue

        # sort fields to keep required ones on top
        if 'required' in s:
            required = s['required']
        elif 'allOf' in s:
            try:
                required = s['allOf'][1]['required']
            except KeyError:
                # no required field
                continue
        else:
            continue

        sorted_props = {}
        optional = {}
        for prop, value in properties.items():
            if prop in required:
                sorted_props[prop] = value
            else:
                optional[prop] = value

        sorted_props.update(optional)

        properties = dict(sorted_props)

    tag_names.sort()
    open_api['tags'] = tags
    open_api['x-tagGroups'][0]['tags'] = tag_names

    open_api['components']['schemas'] = schemas

    return open_api


def get_schemas_inheritance(model_cls):
    """This method modifies the default OpenAPI from Pydantic.

    It adds referenced values to subclasses using allOf field as explained in this post:
    https://swagger.io/docs/specification/data-models/inheritance-and-polymorphism
    """
    model = get_model(model_cls[0])
    flat_models = get_flat_models_from_model(model)

    # this is the list of all the referenced objects
    model_name_map = get_model_name_map(flat_models)
    # flip the dictionary so I can access each class by name
    model_name_map = {v: k for k, v in model_name_map.items()}
    # list of top level class names that we should stop at
    stoppage = set(['NoExtraBaseModel', 'ModelMetaclass', 'BaseModel', 'object'])

    # Pydantic does not necessarily add all the baseclasses to the OpenAPI documentation.
    # We check all of them and them to the list if they are not already added
    models = list(model_name_map.values())
    for model in models:
        for cls in type.mro(model):
            if cls.__name__ in stoppage:
                break
            if cls.__name__ not in model_name_map:
                model_name_map[cls.__name__] = cls

    # get the standard OpenAPI schema for Pydantic for all the new objects
    ref_prefix = '#/components/schemas/'
    schemas = \
        schema(model_name_map.values(), ref_prefix=ref_prefix)['definitions']

    # this is the list of special keys that we copy in manually
    copied_keys = set(['type', 'properties', 'required'])

    # iterate through all the data models
    # find the ones which are subclassed and updated them based on the properties of
    # baseclasses.
    for name in schemas.keys():
        # find the class from class name
        main_cls = model_name_map[name]
        top_classes = []
        for cls in type.mro(main_cls):
            if cls.__name__ in stoppage:
                break
            top_classes.append(cls)
        if len(top_classes) < 2:
            # this class is not a subclass
            print(f'\n{name} is not a subclass.')
            continue

        # remove the class itself
        print(f'\nProcessing {name}')
        top_classes = top_classes[1:]
        top_class = top_classes[0]
        tree = ['....' * (i + 1) + c.__name__ for i, c in enumerate(top_classes)]
        print('\n'.join(tree))

        # collect required and properties from top classes so we don't end up with
        # duplicate values in the schema for the subclass
        top_classes_required = []
        top_classes_prop = {}

        for t in top_classes:
            if 'required' in schemas[t.__name__]:
                tc_required = schemas[t.__name__]['required']
            elif 'allOf' in schemas[t.__name__]:
                try:
                    tc_required = schemas[t.__name__]['allOf'][1]['required']
                except KeyError:
                    # no required field
                    tc_required = []
            else:
                continue

            for r in tc_required:
                top_classes_required.append(r)

        for t in top_classes:
            if 'properties' in schemas[t.__name__]:
                tc_prop = schemas[t.__name__]['properties']
            else:
                tc_prop = schemas[t.__name__]['allOf'][1]['properties']

            for pn, dt in tc_prop.items():
                # collect type to find the cases when the property has the same name
                # but is defined with a different type
                if 'type' in dt:
                    top_classes_prop[pn] = dt['type']
                else:
                    top_classes_prop[pn] = '###'  # no type means use of oneOf or allOf

        # create a new schema for this object based on the top level class
        data = {
            'allOf': [
                {
                    '$ref': f'#/components/schemas/{top_class.__name__}'
                },
                {
                    'type': 'object',
                    'required': [],
                    'properties': {}
                }
            ]
        }

        data_copy = dict(data)
        # the immediate top class openapi schema
        object_dict = schemas[name]

        if not top_classes_required and 'required' in object_dict:
            # no required in top level class
            for r in object_dict['required']:
                data_copy['allOf'][1]['required'].append(r)
        elif 'required' in object_dict and top_classes_required:
            for r in object_dict['required']:
                if r not in top_classes_required:
                    data_copy['allOf'][1]['required'].append(r)

        # no required fields
        if len(data_copy['allOf'][1]['required']) == 0:
            del(data_copy['allOf'][1]['required'])

        if 'properties' in object_dict:
            properties = object_dict['properties']
        else:
            # the top class is a subclass itself
            # properties are under allOf field
            properties = object_dict['allOf'][1]['properties']

        for prop in properties:
            if prop not in top_classes_prop:
                # new field. add it to the properties
                print(f'Extending: {prop}')
                data_copy['allOf'][1]['properties'][prop] = properties[prop]
            elif 'type' not in properties[prop] and \
                    ('allOf' in properties[prop] or 'anyOf' in properties[prop]):
                # same name diffrent types
                print(f'Updating: {prop}')
                data_copy['allOf'][1]['properties'][prop] = properties[prop]

        try:
            data_copy['allOf'][1]['properties']['type'] = properties['type']
        except KeyError:
            print(f'Found object with no type:{name}')

        # add other items in addition to copied_keys
        for key, value in schemas[name].items():
            if key in copied_keys:
                continue
            data_copy[key] = value

        schemas[name] = data_copy

    return schemas
