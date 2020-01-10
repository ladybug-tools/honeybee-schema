"""Programtype Schema"""
from pydantic import Field, constr

from ._base import NamedEnergyBaseModel
from .load import PeopleAbridged, LightingAbridged, ElectricEquipmentAbridged, \
    GasEquipmentAbridged, InfiltrationAbridged, VentilationAbridged, SetpointAbridged


class ProgramTypeAbridged(NamedEnergyBaseModel):

    type: constr(regex='^ProgramTypeAbridged$') = 'ProgramTypeAbridged'
    
    people: PeopleAbridged = Field(
        default = None,
        description='People to describe the occupancy of the program. If None, '
            'no occupancy will be assumed for the program.'
    )

    lighting: LightingAbridged = Field(
        default = None,
        description='Lighting to describe the lighting usage of the program. '
            'If None, no lighting will be assumed for the program.'
    )

    electrical_equipment: ElectricEquipmentAbridged = Field(
        default = None,
        description='ElectricEquipment to describe the usage of electric equipment '
            'within the program. If None, no electric equipment will be assumed.'
    )

    gas_equipment: GasEquipmentAbridged = Field(
        default = None,
        description='GasEquipment to describe the usage of gas equipment '
            'within the program. If None, no gas equipment will be assumed.'
    )

    infiltration : InfiltrationAbridged = Field(
        default = None,
        description='Infiltration to describe the outdoor air leakage of '
            'the program. If None, no infiltration will be assumed for the program.'
    )

    ventilation : VentilationAbridged = Field(
        default = None,
        description='Ventilation to describe the minimum outdoor air requirement '
            'of the program. If None, no ventilation requirement will be assumed.'
    )

    setpoint: SetpointAbridged = Field(
        default = None,
        description='Setpoint object to describe the temperature and humidity setpoints '
            'of the program.  If None, the ProgramType cannot be assigned to a Room '
            'that is conditioned.'
    )


if __name__ == '__main__':
    print(ProgramTypeAbridged.schema_json(indent=2))
