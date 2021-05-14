"""Changes associated with version Honeybee schema version 1.43.5."""


def version_1_43_5(model_dict):
    """Implement changes in a Model dict to make it compatible with version 1.43.5."""
    if 'radiance' in model_dict['properties']:
        if 'modifiers' in model_dict['properties']['radiance']:
            for mod in model_dict['properties']['radiance']['modifiers']:
                if mod['type'] != 'BSDF':
                    mod['type'] = mod['type'].capitalize()
    return model_dict
