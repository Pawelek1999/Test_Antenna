import pytest
import logging
import pythoncom
from drivers.rs_smb100a import SMB100A
from drivers.ni.do_9485 import NI9485Handler
from drivers.ni.usb_6361 import NIUSB6361Handler
from drivers.ui.ctrl_axes import CtrlAxesDriver

_LOGGER = logging.getLogger("EMC.Fixtures")


@pytest.fixture(scope="function")
def generator(hardware_config):
    """
    Provides an SMB100A generator driver instance.
    Ensures the generator is set to a safe state (RF OFF, Min Power) after each test.
    """
    address = hardware_config["generator_address"]
    if not address:
        pytest.skip(
            "Generator address not configured in pytest.ini or environment variables."
        )

    _LOGGER.info(f"Initializing SMB100A Generator at resource: {address}...")
    try:
        driver = SMB100A(address)
    except Exception as e:
        pytest.fail(f"Could not connect to Generator: {e}")

    yield driver

    _LOGGER.info("Teardown: Setting Generator to Safe State.")
    driver.safe_state()
    driver.close()


@pytest.fixture(scope="function")
def ni_relay(hardware_config):
    """
    Provides an NI 9485 Relay driver instance.
    Ensures all relays are OPEN after each test for safety.
    """
    device_id = hardware_config["ni_relay_id"]
    if not device_id:
        pytest.skip(
            "NI Relay Device ID not configured in pytest.ini or environment variables."
        )

    _LOGGER.info(f"Initializing NI 9485 Relay Card (Device ID: {device_id})...")
    driver = NI9485Handler(device_id)
    yield driver

    _LOGGER.info("Teardown: Opening all relays.")
    driver.safe_state()


@pytest.fixture(scope="function")
def ni_analog(hardware_config):
    """
    Provides an NI USB-6361 Analog Input driver instance.
    Performs a health check (safe state verification) after each test.
    """
    device_id = hardware_config["ni_analog_id"]
    if not device_id:
        pytest.skip(
            "NI Analog Device ID not configured in pytest.ini or environment variables."
        )

    _LOGGER.info(f"Initializing NI USB-6361 Analog Card (Device ID: {device_id})...")
    driver = NIUSB6361Handler(device_id)
    yield driver

    _LOGGER.info("Teardown: Verifying NI Analog safe state.")
    driver.safe_state()


@pytest.fixture(scope="session")
def ctrl_axes():
    """
    Provides a CtrlAxes UI Driver instance.
    Assumes the CtrlAxes application is already running.
    Ensures all movement is stopped after each test.
    """
    _LOGGER.info("Connecting to CtrlAxes Application...")
    driver = CtrlAxesDriver()
    driver.start_or_attach(
        app_exe="C:\\AcEmcV7\\CtrlAxesV7.exe",
        app_name=r"Somfy_Pologne.cmp - CtrlAxesV7.*",
    )
    yield driver

    _LOGGER.info("Teardown: Stopping CtrlAxes movement.")
    driver.click_button_stop()
