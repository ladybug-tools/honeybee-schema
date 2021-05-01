"""Changes associated with version Honeybee schema version 1.43.1."""

NEW_ABRIDGED_CLASSES = ('FCUwithDOAS', 'VRFwithDOAS', 'WSHPwithDOAS')


def version_1_43_1(model_dict):
    """Implement changes in a Model dict to make it compatible with version 1.43.1."""
    if 'energy' in model_dict['properties']:
        if 'hvacs' in model_dict['properties']['energy']:
            for hvac in model_dict['properties']['energy']['hvacs']:
                if hvac['type'] in NEW_ABRIDGED_CLASSES:
                    hvac['type'] = '{}Abridged'.format(hvac['type'])
                if 'economizer_type' in hvac and hvac['economizer_type'] == 'Inferred':
                    hvac['economizer_type'] = 'NoEconomizer'
                for prop in ('sensible_heat_recovery', 'latent_heat_recovery'):
                    if prop in hvac and not isinstance(hvac[prop], (float, int)):
                        hvac[prop] = 0
    return model_dict
