"""Programtype Schema"""
from pydantic import Schema
from enum import Enum

from ._base import NamedEnergyBaseModel
from .load import PeopleAbridged, LightingAbridged, ElectricEquipmentAbridged, \
    GasEquipmentAbridged, InfiltrationAbridged, VentilationAbridged, SetpointAbridged


class ProgramTypeAbridged(NamedEnergyBaseModel):

    type: Enum('ProgramTypeAbridged', {'type': 'ProgramTypeAbridged'})
    
    people: PeopleAbridged = Schema(
        default = None,
        description='People to describe the occupancy of the program. If None, '
            'no occupancy will be assumed for the program.'
    )

    lighting: LightingAbridged = Schema(
        default = None,
        description='Lighting to describe the lighting usage of the program. '
            'If None, no lighting will be assumed for the program.'
    )

    electrical_equipment: ElectricEquipmentAbridged = Schema(
        default = None,
        description='ElectricEquipment to describe the usage of electric equipment '
            'within the program. If None, no electric equipment will be assumed.'
    )

    gas_equipment: GasEquipmentAbridged = Schema(
        default = None,
        description='GasEquipment to describe the usage of gas equipment '
            'within the program. If None, no gas equipment will be assumed.'
    )

    infiltration : InfiltrationAbridged = Schema(
        default = None,
        description='Infiltration to describe the outdoor air leakage of '
            'the program. If None, no infiltration will be assumed for the program.'
    )

    ventilation : VentilationAbridged = Schema(
        default = None,
        description='Ventilation to describe the minimum outdoor air requirement '
            'of the program. If None, no ventilation requirement will be assumed.'
    )

    setpoint: SetpointAbridged = Schema(
        default = None,
        description='Setpoint object to describe the temperature and humidity setpoints '
            'of the program.  If None, the ProgramType cannot be assigned to a Room '
            'that is conditioned.'
    )


if __name__ == '__main__':
    print(ProgramTypeAbridged.schema_json(indent=2))
