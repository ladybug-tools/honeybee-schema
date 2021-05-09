"""Changes associated with version Honeybee schema version 1.43.2."""
UPDATED_CONSTRUCTS = ('OpaqueConstructionAbridged', 'WindowConstructionAbridged')


def version_1_43_2(model_dict):
    """Implement changes in a Model dict to make it compatible with version 1.43.2."""
    if 'energy' in model_dict['properties']:
        if 'constructions' in model_dict['properties']['energy']:
            for construct in model_dict['properties']['energy']['constructions']:
                if construct['type'] in UPDATED_CONSTRUCTS:
                    construct['materials'] = construct.pop('layers')
    return model_dict
