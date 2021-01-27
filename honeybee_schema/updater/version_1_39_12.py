"""Changes associated with version Honeybee schema version 1.39.12."""


def version_1_39_12(model_dict):
    """Implement changes in a Model dict to make it compatible with version 1.39.12."""
    removed_equip = 'PSZ-AC district chilled water with baseboard district hot water'
    replaced_equip = 'PSZ-AC district chilled water with district hot water'
    if 'energy' in model_dict['properties']:
        if 'hvacs' in model_dict['properties']['energy']:
            for hvac in model_dict['properties']['energy']['hvacs']:
                if hvac['type'] != 'IdealAirSystemAbridged' and \
                        hvac['equipment_type'] == removed_equip:
                    hvac['equipment_type'] = replaced_equip
    return model_dict
