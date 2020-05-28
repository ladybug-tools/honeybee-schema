# coding=utf-8
from honeybee_energy.simulation.parameter import SimulationParameter
from honeybee_energy.simulation.output import SimulationOutput
from honeybee_energy.simulation.runperiod import RunPeriod
from honeybee_energy.simulation.daylightsaving import DaylightSavingTime
from honeybee_energy.simulation.control import SimulationControl
from honeybee_energy.simulation.shadowcalculation import ShadowCalculation
from honeybee_energy.simulation.sizing import SizingParameter

from ladybug.dt import Date

import os
import json


def simulation_par_simple(directory):
    sim_par = SimulationParameter()

    dest_file = os.path.join(directory, 'simulation_par_simple.json')
    with open(dest_file, 'w') as fp:
        json.dump(sim_par.to_dict(), fp, indent=4)


def simulation_par_detailed(directory):
    sim_par = SimulationParameter()
    output = SimulationOutput()
    output.add_zone_energy_use()
    output.include_html = True
    output.reporting_frequency = 'Daily'
    output.add_summary_report('Annual Building Utility Performance Summary')
    output.add_summary_report('Climatic Data Summary')
    output.add_summary_report('Envelope Summary')
    sim_par.output = output
    run_period = RunPeriod(Date(1, 1), Date(6, 21))
    run_period.daylight_saving_time = DaylightSavingTime(Date(3, 12), Date(11, 5))
    run_period.start_day_of_week = 'Monday'
    run_period.holidays = [Date(1, 1), Date(3, 17), Date(7, 4)]
    sim_par.run_period = run_period
    sim_par.timestep = 4
    sim_control_alt = SimulationControl(run_for_sizing_periods=True,
                                        run_for_run_periods=False)
    sim_par.simulation_control = sim_control_alt
    shadow_calc_alt = ShadowCalculation(
        solar_distribution='FullInteriorAndExteriorWithReflections',
        calculation_method='PixelCounting', calculation_update_method='Timestep')
    sim_par.shadow_calculation = shadow_calc_alt
    sizing_alt = SizingParameter(None, 1, 1)
    relative_path = './scripts/ddy/chicago.ddy'
    sizing_alt.add_from_ddy_996_004(relative_path)
    sim_par.sizing_parameter = sizing_alt

    dest_file = os.path.join(directory, 'simulation_par_detailed.json')
    with open(dest_file, 'w') as fp:
        json.dump(sim_par.to_dict(), fp, indent=4)


# run all functions within the file
master_dir = os.path.split(os.path.dirname(__file__))[0]
sample_directory = os.path.join(master_dir, 'samples', 'simulation_parameter')

simulation_par_simple(sample_directory)
simulation_par_detailed(sample_directory)
