import enum
import logging

from RsInstrument import RsInstrument

_LOGGER = logging.getLogger(__name__)


class InstrumentError(Exception):
    """Base exception class for instrument-related errors."""

    pass


class InstrumentConnectionError(InstrumentError):
    """Raised when the connection to the instrument cannot be established."""

    pass


class InstrumentCommandError(InstrumentError):
    """Raised when an SCPI command execution fails."""

    pass


class InstrumentRangeError(InstrumentError):
    """Raised when a requested value is outside the instrument's physical limits."""

    pass


class CommonOrders(enum.StrEnum):
    """Standard IEEE 488.2 common commands."""

    IDN = "*IDN?"
    RESET = "*RST"
    OPC = "*OPC?"
    ERROR = "SYST:ERR?"


class InstrumentOrders(enum.StrEnum):
    """SCPI commands specific to the Rohde & Schwarz SMB100A generator."""

    RF_ON = "OUTP ON"
    RF_OFF = "OUTP OFF"
    RF_STATE = "OUTP?"
    FREQ_SET = "FREQ {}"
    FREQ_GET = "FREQ?"
    POW_SET = "POW {}"
    POW_GET = "POW?"


class SMB100A:
    """Driver class for the Rohde & Schwarz SMB100A Signal Generator.

    This class provides a high-level API to control RF output state,
    frequency, and power levels using SCPI commands over the RsInstrument library.
    """

    def __init__(self, resource: str, timeout_ms: int = 5000):
        """Initializes the connection to the SMB100A generator.

        Args:
            resource: The VISA resource address (e.g., 'TCPIP::192.168.1.10::INSTR').
            timeout_ms: Communication timeout in milliseconds.

        Raises:
            InstrumentConnectionError: If the connection to the instrument fails.
        """
        _LOGGER.debug(f"Initializing SMB100A generator at resource: {resource}")
        try:
            self.inst = RsInstrument(resource)
            self.inst.visa_timeout = timeout_ms
        except Exception as exc:
            raise InstrumentConnectionError(f"Cannot connect to SMB100A at resource {resource}") from exc
        _LOGGER.debug("Instrument initialized successfully.")

    def __enter__(self):
        """Context manager entry point."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Ensures the instrument is left in a safe state and closed."""
        self.safe_state()
        self.close()

    def safe_state(self) -> None:
        """Sets the instrument to a safe state (RF Output OFF, Min Power).

        This method is critical for BDD-style testing to ensure the laboratory
        setup remains safe after test execution or in case of failure.
        """
        _LOGGER.info("Setting SMB100A to safe state.")
        try:
            self.set_output_rf(False)
            self.set_power(-120)
        except InstrumentError as exc:
            _LOGGER.error(f"Failed to reach safe state: {exc}")

    def close(self):
        """Closes the communication session with the instrument."""
        try:
            self.inst.close()
            _LOGGER.debug("Instrument session closed.")
        except Exception:
            pass

    def get_idn(self) -> str:
        """Queries the instrument identification string (*IDN?).

        Returns:
            The identification string containing manufacturer, model, and serial.
        """
        return self._query_str(CommonOrders.IDN)

    def get_output_rf_state(self) -> bool:
        """Gets the current RF output state.

        Returns:
            True if RF output is ON, False otherwise.
        """
        rf_en = self._query_bool(InstrumentOrders.RF_STATE)
        _LOGGER.debug(f"RF Output state: {'ON' if rf_en else 'OFF'}")
        return rf_en

    def set_output_rf(self, state: bool) -> None:
        """Enables or disables the RF output emission.

        Args:
            state: True to enable RF output, False to disable.
        """
        _LOGGER.info(f"Setting RF Output to: {state}")
        self._write(InstrumentOrders.RF_ON if state else InstrumentOrders.RF_OFF)

    def get_frequency(self) -> float:
        """Gets the current RF frequency.

        Returns:
            The frequency value in Hertz (Hz).
        """
        return self._query_float(InstrumentOrders.FREQ_GET)

    def set_frequency(self, hz: float) -> None:
        """Sets the RF frequency.

        Args:
            hz: Frequency value in Hertz.

        Raises:
            InstrumentRangeError: If frequency is less than or equal to 0.
        """
        if hz <= 0:
            raise InstrumentRangeError(f"Frequency {hz} Hz must be greater than 0.")
        _LOGGER.debug(f"Setting frequency to: {hz} Hz")
        self._write(InstrumentOrders.FREQ_SET.format(f"{hz:.2f}"))

    def get_power(self) -> float:
        """Gets the current RF power level.

        Returns:
            The power level in dBm.
        """
        return self._query_float(InstrumentOrders.POW_GET)

    def set_power(self, dbm: float) -> None:
        """Sets the RF power level.

        Args:
            dbm: Power level in dBm (Range: -120 to 14).

        Raises:
            InstrumentRangeError: If power level is outside the allowed range.
        """
        if not -120 <= dbm <= 20:
            raise InstrumentRangeError(f"Power {dbm} dBm is out of range (-120 to 14).")
        _LOGGER.debug(f"Setting power to: {dbm} dBm")
        self._write(InstrumentOrders.POW_SET.format(f"{dbm:.2f}"))

    def _write(self, cmd: str) -> None:
        """Writes an SCPI command and waits for completion (*OPC?).

        Args:
            cmd: SCPI command string.

        Raises:
            InstrumentCommandError: If the write operation or OPC synchronization fails.
        """
        try:
            self.inst.write_with_opc(cmd)
        except Exception as exc:
            raise InstrumentCommandError(f"SCPI write failed: {cmd}") from exc

    def _query_float(self, cmd: str) -> float:
        """Queries the instrument and converts the response to a float.

        Args:
            cmd: SCPI query string.

        Returns:
            The queried value as a float.
        """
        try:
            return self.inst.query_float_with_opc(cmd)
        except Exception as exc:
            raise InstrumentCommandError(f"SCPI query float failed: {cmd}") from exc

    def _query_bool(self, cmd: str) -> bool:
        """Queries the instrument and converts the response to a boolean.

        Args:
            cmd: SCPI query string.

        Returns:
            The queried value as a bool.
        """
        try:
            return self.inst.query_bool_with_opc(cmd)
        except Exception as exc:
            raise InstrumentCommandError(f"SCPI query bool failed: {cmd}") from exc

    def _query_str(self, cmd: str) -> str:
        """Queries the instrument and returns the response as a stripped string.

        Args:
            cmd: SCPI query string.

        Returns:
            The queried value as a string.
        """
        try:
            return self.inst.query_str_with_opc(cmd).strip()
        except Exception as exc:
            raise InstrumentCommandError(f"SCPI query string failed: {cmd}") from exc
