import logging
import nidaqmx
from drivers.ni.exceptions import NIError, NIConfigurationError, NIOperationError

_LOGGER = logging.getLogger(__name__)


class NI9485Handler:
    """
    Handler for the NI 9485 8-channel SSR Relay Module.

    This driver is strictly limited to Digital Output (DO) operations,
    matching the hardware capabilities of the NI 9485 relay module.
    """

    def __init__(self, device_id: str):
        """
        Initializes the NI Relay Handler.

        Args:
            device_id: The NI device identifier (e.g., 'Dev1').
        """
        self.device_id = device_id
        _LOGGER.debug(f"Initializing NI 9485 Relay Handler for device: {device_id}")

    def write_relay(self, line: int, state: bool) -> None:
        """
        Sets the state of a single relay channel.

        Args:
            line: The relay channel number (0 to 7).
            state: True to close the relay (ON), False to open it (OFF).

        Raises:
            NIConfigurationError: If the specified channel path is invalid.
            NIOperationError: If the physical switching operation fails.
            NIError: For other unexpected NI-DAQmx errors.
        """
        # The NI 9485 module typically uses port0 for all its relay lines.
        line_path = f"{self.device_id}/port0/line{line}"
        _LOGGER.debug(f"Switching relay {line_path} to {'ON' if state else 'OFF'}")

        try:
            with nidaqmx.Task() as task:
                try:
                    task.do_channels.add_do_chan(line_path)
                except nidaqmx.DaqError as exc:
                    raise NIConfigurationError(f"Failed to configure relay line: {line_path}") from exc

                try:
                    task.write(state)
                except nidaqmx.DaqError as exc:
                    raise NIOperationError(f"Physical switching failed on line: {line_path}") from exc

        except nidaqmx.DaqError as exc:
            raise NIError(f"An unexpected NI 9485 error occurred: {exc}") from exc

    def safe_state(self) -> None:
        """
        Sets the device to a safe state by opening all relays (OFF).

        This is a critical method for ensuring that all connected peripherals
        or power supplies are disconnected in case of test failure or completion.
        """
        _LOGGER.info(f"Setting safe state on NI 9485 ({self.device_id}): Opening all relays.")
        try:
            # Writing 0 to the entire port 0 turns off all 8 relays (0x00).
            port_path = f"{self.device_id}/port0"
            with nidaqmx.Task() as task:
                task.do_channels.add_do_chan(port_path)
                task.write(0)
        except Exception as exc:
            _LOGGER.error(f"Critical failure: Could not open all relays during safe_state: {exc}")
