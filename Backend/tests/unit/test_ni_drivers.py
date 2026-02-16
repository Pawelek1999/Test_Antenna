import pytest
from unittest.mock import patch, MagicMock, ANY
from drivers.ni.do_9485 import NI9485Handler
from drivers.ni.usb_6361 import NIUSB6361Handler
from drivers.ni.exceptions import NIConfigurationError, NIOperationError

DEVICE_ID = "DevMock"

class MockDaqError(Exception):
    """Custom exception to simulate nidaqmx.DaqError."""
    pass

@pytest.fixture
def mock_nidaqmx_task():
    """Mocks the nidaqmx.Task context manager."""
    with patch("drivers.ni.do_9485.nidaqmx") as mock_nidaqmx_do, \
         patch("drivers.ni.usb_6361.nidaqmx") as mock_nidaqmx_ai:
        
        mock_nidaqmx_do.DaqError = MockDaqError
        mock_nidaqmx_ai.DaqError = MockDaqError
        
        mock_task = MagicMock()
        mock_nidaqmx_do.Task.return_value.__enter__.return_value = mock_task
        mock_nidaqmx_ai.Task.return_value.__enter__.return_value = mock_task
        
        yield mock_task

# --- NI9485Handler (Relay) Tests ---

def test_ni9485_write_relay_success(mock_nidaqmx_task):
    """Verifies a successful relay write operation."""
    driver = NI9485Handler(DEVICE_ID)
    driver.write_relay(line=3, state=True)
    
    mock_nidaqmx_task.do_channels.add_do_chan.assert_called_with(f"{DEVICE_ID}/port0/line3")
    mock_nidaqmx_task.write.assert_called_with(True)

def test_ni9485_write_relay_config_error(mock_nidaqmx_task):
    """Verifies that a configuration error is handled correctly."""
    mock_nidaqmx_task.do_channels.add_do_chan.side_effect = MockDaqError("Invalid channel")
    
    driver = NI9485Handler(DEVICE_ID)
    with pytest.raises(NIConfigurationError):
        driver.write_relay(line=99, state=True)

def test_ni9485_write_relay_operation_error(mock_nidaqmx_task):
    """Verifies that a write operation error is handled correctly."""
    mock_nidaqmx_task.write.side_effect = MockDaqError("Hardware failure")
    
    driver = NI9485Handler(DEVICE_ID)
    with pytest.raises(NIOperationError):
        driver.write_relay(line=1, state=False)

def test_ni9485_safe_state(mock_nidaqmx_task):
    """Verifies that safe_state opens all relays."""
    driver = NI9485Handler(DEVICE_ID)
    driver.safe_state()
    
    mock_nidaqmx_task.do_channels.add_do_chan.assert_called_with(f"{DEVICE_ID}/port0")
    mock_nidaqmx_task.write.assert_called_with(0)

# --- NIUSB6361Handler (Analog Input) Tests ---

def test_ni6361_read_analog_success(mock_nidaqmx_task):
    """Verifies a successful analog read operation."""
    mock_nidaqmx_task.read.return_value = 5.123
    
    driver = NIUSB6361Handler(DEVICE_ID)
    voltage = driver.read_analog_input(channel=2)
    
    assert voltage == 5.123
    mock_nidaqmx_task.ai_channels.add_ai_voltage_chan.assert_called_once()
    mock_nidaqmx_task.read.assert_called_once()

def test_ni6361_read_analog_config_error(mock_nidaqmx_task):
    """Verifies that an AI channel configuration error is handled correctly."""
    mock_nidaqmx_task.ai_channels.add_ai_voltage_chan.side_effect = MockDaqError("Invalid AI channel")
    
    driver = NIUSB6361Handler(DEVICE_ID)
    with pytest.raises(NIConfigurationError):
        driver.read_analog_input(channel=99)

def test_ni6361_safe_state_verification(mock_nidaqmx_task):
    """Verifies that safe_state performs a verification read."""
    driver = NIUSB6361Handler(DEVICE_ID)
    driver.safe_state()
    
    mock_nidaqmx_task.ai_channels.add_ai_voltage_chan.assert_called_with(
        f"{DEVICE_ID}/ai0", min_val=-10.0, max_val=10.0, units=ANY, terminal_config=ANY
    )
    mock_nidaqmx_task.read.assert_called_once()
