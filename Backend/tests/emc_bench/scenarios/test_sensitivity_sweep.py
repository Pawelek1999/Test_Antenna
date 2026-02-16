import pytest
import logging
import time
import os
from datetime import datetime
from reporting.result_collector import ResultCollector

# Import steps
import tests.emc_bench.bdd_steps.application_ctrl_axes as axes_steps
import tests.emc_bench.bdd_steps.generator_smb100a as gen_steps
import tests.emc_bench.bdd_steps.ni_cards as ni_steps
from paths import RESULTS_DIR

_LOGGER = logging.getLogger("Test.SensitivitySweep")

# Test Constants
START_FREQ_HZ = 869.8e6
START_POWER_DBM = -80.0
END_POWER_DBM = 10.0
POWER_STEP_DB = 1.0
VOLTAGE_THRESHOLD_V = 2.5
ANALOG_CHANNEL = 0


@pytest.mark.emc_bench
def test_sensitivity_sweep(generator, ni_relay, ni_analog, ctrl_axes):
    """
    Performs a sensitivity sweep test for both Horizontal and Vertical polarizations
    and saves the results to a timestamped JSON file.
    """

    # --- 1. SETUP ---
    _LOGGER.info("=== Step 1: Initializing Test Bench Setup ===")
    collector = ResultCollector()

    gen_steps.set_generator_frequency(generator, START_FREQ_HZ)
    gen_steps.set_generator_power(generator, START_POWER_DBM)
    gen_steps.disable_rf_output(generator)
    ni_steps.open_all_relays(ni_relay)

    # --- 2. EXECUTION SEQUENCE ---
    target_angles = range(0, 330, 30)
    polarizations = [("V", axes_steps.move_malt_to_vertical_polar), ("H", axes_steps.move_malt_to_horizontal_polar)]

    gen_steps.enable_rf_output(generator)

    for angle in target_angles:
        _LOGGER.info(f"=== Testing Angle: {angle} degrees ===")
        axes_steps.move_turntable_to_position(ctrl_axes, angle)
        axes_steps.wait_turntable_reach_position(ctrl_axes, angle)

        for polar_code, set_polar_func in polarizations:
            _LOGGER.info(f"--- Testing Polarization: {polar_code} ---")
            set_polar_func(ctrl_axes)
            time.sleep(1)

            activation_power = None
            stop_power = None

            current_power = START_POWER_DBM
            gen_steps.set_generator_power(generator, current_power)

            while current_power <= END_POWER_DBM:
                voltage = ni_steps.measure_voltage(ni_analog, ANALOG_CHANNEL)
                if voltage >= VOLTAGE_THRESHOLD_V:
                    _LOGGER.info(f"Activation detected at {current_power:.2f} dBm.")
                    activation_power = current_power
                    break
                current_power += POWER_STEP_DB
                gen_steps.set_generator_power(generator, current_power)
                time.sleep(0.05)

            if activation_power is not None:
                stop_power = activation_power - 10  # Placeholder for actual stop power logic
                _LOGGER.info(f"Simulated stop power at {stop_power:.2f} dBm.")

            collector.add_measurement(angle, polar_code, activation_power or 0, stop_power or 0)

    # --- 3. TEARDOWN ---
    _LOGGER.info("=== Test Sequence Complete ===")
    gen_steps.disable_rf_output(generator)
    axes_steps.move_turntable_to_position(ctrl_axes, 0)

    # --- 4. SAVE REPORT ---
    final_json = collector.to_json()
    _LOGGER.info("--- Final JSON Report ---")
    _LOGGER.info(final_json)

    # Create a unique filename with a timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"sensitivity_sweep_{timestamp}.json"

    # Create the results directory if it doesn't exist
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)

    report_path = os.path.join(RESULTS_DIR, filename)

    try:
        with open(report_path, "w") as f:
            f.write(final_json)
        _LOGGER.info(f"Report successfully saved to: {report_path}")
    except IOError as e:
        _LOGGER.error(f"Failed to save report to {report_path}: {e}")

    assert len(collector.get_data()) == len(target_angles)
