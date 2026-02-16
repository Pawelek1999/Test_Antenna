import logging
import nidaqmx
from nidaqmx.constants import TerminalConfiguration, VoltageUnits

from drivers.ni.exceptions import NIError, NIConfigurationError, NIOperationError

_LOGGER = logging.getLogger(__name__)


class NIUSB6361Handler:
    """
    Handler for NI-USB-6361 Analog Input operations.

    This driver is restricted to Analog Input (AI) functionality to maintain
    minimalism and safety in the EMC laboratory environment.
    """

    def __init__(self, device_id: str):
        """
        Initializes the NI Analog Input Handler.

        Args:
            device_id: The NI device identifier (e.g., 'Dev1').
        """
        self.device_id = device_id
        _LOGGER.debug(f"Initializing NI-USB-6361 Analog Input Handler for device: {device_id}")

    def read_analog_input(
        self,
        channel: int,
        min_val: float = -10.0,
        max_val: float = 10.0,
        differential: bool = True,
    ) -> float:
        """
        Reads a single analog voltage sample from the specified channel.

        Args:
            channel: The analog input channel number (e.g., 0 for 'ai0').
            min_val: The minimum expected voltage value.
            max_val: The maximum expected voltage value.
            differential: If True (default), uses Differential mode. Otherwise, uses RSE.

        Returns:
            The measured voltage value in Volts.

        Raises:
            NIConfigurationError: If the channel configuration fails.
            NIOperationError: If the physical read operation fails.
            NIError: For other unexpected NI-DAQmx errors.
        """
        channel_path = f"{self.device_id}/ai{channel}"
        term_config = TerminalConfiguration.DIFF if differential else TerminalConfiguration.RSE

        try:
            with nidaqmx.Task() as task:
                # 1. Configuration Phase
                try:
                    task.ai_channels.add_ai_voltage_chan(
                        channel_path,
                        min_val=min_val,
                        max_val=max_val,
                        units=VoltageUnits.VOLTS,
                        terminal_config=term_config,
                    )
                except nidaqmx.DaqError as exc:
                    raise NIConfigurationError(f"Failed to configure AI channel: {channel_path}") from exc

                # 2. Execution Phase
                try:
                    return task.read()
                except nidaqmx.DaqError as exc:
                    raise NIOperationError(f"Failed to read from AI channel: {channel_path}") from exc

        except nidaqmx.DaqError as exc:
            raise NIError(f"An unexpected NI error occurred on {channel_path}: {exc}") from exc

    def safe_state(self) -> None:
        """
        Verifies that the analog input hardware is responsive.

        Since AI is a passive measurement, this method performs a connectivity check
        (dummy read) to ensure the hardware is alive and communicating.
        """
        _LOGGER.debug(f"Verifying safe state (connectivity check) for NI-USB-6361 ({self.device_id}).")
        try:
            # Perform a dummy read on channel 0 to verify device health.
            self.read_analog_input(0)
            _LOGGER.debug("Hardware communication verified successfully.")
        except Exception as exc:
            _LOGGER.error(f"Hardware health check failed: {exc}")
