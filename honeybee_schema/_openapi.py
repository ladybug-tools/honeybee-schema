from pydantic.utils import get_model
from pydantic.schema import schema, get_flat_models_from_model, get_model_name_map
from typing import Dict, List, Any
import enum

# base open api dictionary for all schemas
_base_open_api = {
    "openapi": "3.0.2",
    "servers": [],
    "info": {},
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
    base_object: List[Any],
    title: str = None,
    version: str = None,
    openapi_version: str = "3.0.2",
    description: str = None,
    info: dict = None,
    external_docs: dict = None,
    inheritance: bool = False
        ) -> Dict:
    """Return Honeybee Model Schema as an openapi compatible dictionary."""
    open_api = dict(_base_open_api)

    open_api['openapi'] = openapi_version

    if info:
        open_api['info'] = info

    if title:
        open_api['info']['title'] = title

    if not version:
        raise ValueError(
            'Schema version must be specified as argument or from distribution metadata'
        )

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
        model_name, tag = create_tag(name)
        tag_names.append(model_name)
        tags.append(tag)

        # sort properties order: put required parameters at begining of the list
        s = schemas[name]

        if 'properties' in s:
            properties = s['properties']
        elif 'enum' in s:
            # enum
            continue
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
        for prop in properties:
            try:
                properties[prop] = set_format(properties[prop])
            except KeyError:
                # referenced object
                if 'anyOf' in properties[prop]:
                    new_any_of = []
                    for item in properties[prop]['anyOf']:
                        new_any_of.append(set_format(item))
                    properties[prop]['anyOf'] = new_any_of
                else:
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

        if 'properties' in s:
            s['properties'] = sorted_props
        else:
            s['allOf'][1]['properties'] = sorted_props

    tag_names.sort()
    open_api['tags'] = tags
    open_api['x-tagGroups'][0]['tags'] = tag_names

    open_api['components']['schemas'] = schemas

    return open_api


def create_tag(name):
    """create a viewer tag from a class name."""
    model_name = '%s_model' % name.lower()
    tag = {
        'name': model_name,
        'x-displayName': name,
        'description':
            '<SchemaDefinition schemaRef=\"#/components/schemas/%s\" />\n' % name
    }
    return model_name, tag


def set_format(p):
    """Set format for a property."""
    if '$ref' in p:
        return p
    elif p['type'] == 'number' and 'format' not in p:
        p['format'] = 'double'
    elif p['type'] == 'integer' and 'format' not in p:
        p['format'] = 'int32'
    elif p['type'] == 'array':
        p['items'] = set_format(p['items'])
    return p


def get_model_mapper(models, stoppage=None, full=True, include_enum=False):
    """Get a dictionary of name: class for all the objects in model."""
    models = [get_model(model) for model in models]
    if include_enum:
        flat_models = [
            m
            for model in models
            for m in get_flat_models_from_model(model)
        ]
    else:
        flat_models = [
            m
            for model in models
            for m in get_flat_models_from_model(model)
            if not isinstance(m, enum.EnumMeta)
        ]

    # this is the list of all the referenced objects
    model_name_map = get_model_name_map(flat_models)
    # flip the dictionary so I can access each class by name
    model_name_map = {v: k for k, v in model_name_map.items()}

    if full:
        if not stoppage:
            stoppage = set(
                [
                    'NoExtraBaseModel', 'ModelMetaclass', 'BaseModel', 'object', 'str',
                    'Enum'
                ]
            )
        # Pydantic does not necessarily add all the baseclasses to the OpenAPI
        # documentation. We check all of them and them to the list if they are not
        # already added
        models = list(model_name_map.values())
        for model in models:
            for cls in type.mro(model):
                if cls.__name__ in stoppage:
                    break
                if cls.__name__ not in model_name_map:
                    model_name_map[cls.__name__] = cls

    return model_name_map


def get_schemas_inheritance(model_cls):
    """This method modifies the default OpenAPI from Pydantic.

    It adds referenced values to subclasses using allOf field as explained in this post:
    https://swagger.io/docs/specification/data-models/inheritance-and-polymorphism
    """
    # list of top level class names that we should stop at
    stoppage = set(['NoExtraBaseModel', 'ModelMetaclass', 'BaseModel', 'object', 'Enum'])

    model_name_map = get_model_mapper(model_cls, stoppage, full=True, include_enum=False)

    # get the standard OpenAPI schema for Pydantic for all the new objects
    ref_prefix = '#/components/schemas/'
    schemas = \
        schema(model_name_map.values(), ref_prefix=ref_prefix)['definitions']

    # collect updated objects
    updated_schemas = {}

    # iterate through all the data models
    # find the ones which are subclassed and updated them based on the properties of
    # baseclasses.
    for name in schemas.keys():
        # find the class from class name
        try:
            main_cls = model_name_map[name]
        except KeyError:
            # enum objects are not included.
            if 'enum' in schemas[name]:
                continue
            raise KeyError(f'{name} key not found.')

        top_classes = []
        for cls in type.mro(main_cls):
            if cls.__name__ in stoppage:
                break
            top_classes.append(cls)
        if len(top_classes) < 2:
            # this class is not a subclass
            print(f'\n{name} is not a subclass.')
            continue
        # set object inheritance
        updated_schema = set_inheritance(name, top_classes, schemas)
        updated_schemas[name] = updated_schema

    # replace updated schemas in original schema
    for name, value in updated_schemas.items():
        schemas[name] = value

    return schemas


def set_inheritance(name, top_classes, schemas):
    """Set inheritance for object with a certain name."""
    # this is the list of special keys that we copy in manually
    copied_keys = set(['type', 'properties', 'required', 'additionalProperties'])
    # remove the class itself
    print(f'\nProcessing {name}')
    top_classes = top_classes[1:]
    top_class = top_classes[0]
    tree = ['....' * (i + 1) + c.__name__ for i, c in enumerate(top_classes)]
    print('\n'.join(tree))

    # the immediate top class openapi schema
    object_dict = schemas[name]
    if 'enum' in object_dict:
        return object_dict

    # collect required and properties from top classes so we don't end up with
    # duplicate values in the schema for the subclass
    top_classes_required = []
    top_classes_prop = {}

    for t in top_classes:
        if 'required' in schemas[t.__name__]:
            tc_required = schemas[t.__name__]['required']
        else:
            continue

        for r in tc_required:
            top_classes_required.append(r)

    for t in top_classes:
        tc_prop = schemas[t.__name__]['properties']

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

    properties = object_dict['properties']

    for prop in properties:
        if prop not in top_classes_prop:
            # new field. add it to the properties
            print(f'Extending: {prop}')
            data_copy['allOf'][1]['properties'][prop] = properties[prop]
        elif 'type' not in properties[prop] and \
                ('allOf' in properties[prop] or 'anyOf' in properties[prop]):
            # same name diffrent types
            print(f'Found a field with the same name: {prop}.')
            if len(top_classes) > 1:
                print(f'Trying {name} against {top_classes[1].__name__}.')
                return set_inheritance(name, top_classes, schemas)
            else:
                return schemas[name]

    try:
        data_copy['allOf'][1]['properties']['type'] = properties['type']
    except KeyError:
        print(f'Found object with no type:{name}')

    if 'additionalProperties' in object_dict:
        data_copy['allOf'][1]['additionalProperties'] = \
            object_dict['additionalProperties']

    # add other items in addition to copied_keys
    for key, value in schemas[name].items():
        if key in copied_keys:
            continue
        data_copy[key] = value
    return data_copy


def class_mapper(models):
    """Create a mapper between OpenAPI models and Python modules.

    This mapper is used by dotnet generator to organize the models under similar
    module structure.
    """

    if not hasattr(models, '__iter__'):
        models = [models]

    mapper = get_model_mapper(models, full=True, include_enum=True)

    # add enum classes to mapper
    schemas = get_schemas_inheritance(models)
    enums = {}
    for name in schemas:
        s = schemas[name]
        if 'enum' in s:
            # add enum
            info = mapper[name]
            if info.__name__ not in enums:
                enums[info.__name__] = info

    module_mapper = {}
    # remove enum from mapper
    classes = {k: c.__module__ for k, c in mapper.items() if k not in enums}
    enums = {k: c.__module__ for k, c in enums.items()}
    # this sorting only works in python3.7+
    module_mapper['classes'] = {k: classes[k] for k in sorted(classes)}
    module_mapper['enums'] = {k: enums[k] for k in sorted(enums)}

    return module_mapper
