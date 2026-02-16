import time
import logging
from typing import TYPE_CHECKING, Callable

from tests.exceptions import UsageStepError, SetupError

if TYPE_CHECKING:
    from drivers.ui.ctrl_axes import CtrlAxesDriver

_LOGGER = logging.getLogger("CtrlAxes.Steps")


def set_mode_turntable(ctrl_axes_app: "CtrlAxesDriver") -> None:
    """
    Switches the application settings to Turntable mode.

    Args:
        ctrl_axes_app: The driver instance for the CtrlAxes application.
    """
    _LOGGER.info("Switching settings to Turntable mode.")
    ctrl_axes_app.set_turntable_settings()
    current = ctrl_axes_app.get_current_settings()
    if current != "Turntable":
        raise SetupError(f"Failed to switch to Turntable mode. Current mode is '{current}'.")


def set_mode_malt(ctrl_axes_app: "CtrlAxesDriver") -> None:
    """
    Switches the application settings to Malt mode.

    Args:
        ctrl_axes_app: The driver instance for the CtrlAxes application.
    """
    _LOGGER.info("Switching settings to Malt mode.")
    ctrl_axes_app.set_malt_settings()
    current = ctrl_axes_app.get_current_settings()
    if current != "Malt":
        raise SetupError(f"Failed to switch to Malt mode. Current mode is '{current}'.")


def verify_setting_mode(ctrl_axes_app: "CtrlAxesDriver", expected_mode: str) -> None:
    """
    Verifies the application is in the expected mode, switching if necessary.

    Args:
        ctrl_axes_app: The driver instance.
        expected_mode: The expected mode ("Turntable" or "Malt").
    """
    allowed_modes = ["Turntable", "Malt"]
    if expected_mode not in allowed_modes:
        raise UsageStepError(f"Invalid mode '{expected_mode}'. Supported modes are: {allowed_modes}.")

    current_mode = ctrl_axes_app.get_current_settings()
    if current_mode != expected_mode:
        _LOGGER.warning(f"Mode mismatch: Expected '{expected_mode}', got '{current_mode}'. Attempting to switch...")
        if expected_mode == "Turntable":
            set_mode_turntable(ctrl_axes_app)
        else:
            set_mode_malt(ctrl_axes_app)
    else:
        _LOGGER.debug(f"Mode verified: {expected_mode}")


def _wait_for_position(get_pos_func: Callable[[], float], target: float, timeout: int) -> None:
    """
    Waits for a device to reach a target position.

    Args:
        get_pos_func: A function that returns the current position.
        target: The target position value.
        timeout: The maximum time to wait in seconds.
    Raises:
        TimeoutError: If the target position is not reached within the timeout.
    """
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            current = get_pos_func()
            if abs(current - target) < 0.01:  # Use a small tolerance for float comparison
                return
            _LOGGER.debug(f"Moving... Current: {current:.2f}, Target: {target:.2f}")
        except Exception as e:
            _LOGGER.warning(f"Could not read position during wait: {e}")
        time.sleep(0.5)

    raise TimeoutError(f"Position {target} not reached within {timeout}s.")


def wait_turntable_reach_position(ctrl_axes_app: "CtrlAxesDriver", target_position: int, timeout: int = 240) -> None:
    """
    Waits for the turntable to reach the specified target position.

    Args:
        ctrl_axes_app: The driver instance.
        target_position: The target position in degrees.
        timeout: The timeout in seconds.
    """
    _LOGGER.info(f"Waiting for turntable to reach {target_position} degrees.")
    verify_setting_mode(ctrl_axes_app, "Turntable")
    _wait_for_position(ctrl_axes_app.get_turntable_degrees, float(target_position), timeout)
    _LOGGER.info("Turntable position reached.")


def wait_malt_reach_position(ctrl_axes_app: "CtrlAxesDriver", target_position: int, timeout: int = 240) -> None:
    """
    Waits for the malt (antenna mast) to reach the specified target position.

    Args:
        ctrl_axes_app: The driver instance.
        target_position: The target height.
        timeout: The timeout in seconds.
    """
    _LOGGER.info(f"Waiting for malt to reach position {target_position}.")
    verify_setting_mode(ctrl_axes_app, "Malt")
    _wait_for_position(ctrl_axes_app.get_malt_height, float(target_position), timeout)
    _LOGGER.info("Malt position reached.")


def stop_movement(ctrl_axes_app: "CtrlAxesDriver") -> None:
    """Triggers the emergency stop."""
    _LOGGER.info("Stopping all movement.")
    ctrl_axes_app.click_button_stop()


def move_turntable_to_position(ctrl_axes_app: "CtrlAxesDriver", position: int) -> None:
    """Moves the turntable to a specific position."""
    _LOGGER.info(f"Moving turntable to {position} degrees.")
    verify_setting_mode(ctrl_axes_app, "Turntable")
    ctrl_axes_app.set_target_position(position)
    ctrl_axes_app.click_btn_move_target_position()


def move_turntable_to_minimum_position(ctrl_axes_app: "CtrlAxesDriver") -> None:
    """Moves the turntable to its minimum position."""
    _LOGGER.info("Moving turntable to minimum position.")
    verify_setting_mode(ctrl_axes_app, "Turntable")
    ctrl_axes_app.move_to_min()


def move_turntable_to_maximum_position(ctrl_axes_app: "CtrlAxesDriver") -> None:
    """Moves the turntable to its maximum position."""
    _LOGGER.info("Moving turntable to maximum position.")
    verify_setting_mode(ctrl_axes_app, "Turntable")
    ctrl_axes_app.move_to_max()


def move_malt_to_position(ctrl_axes_app: "CtrlAxesDriver", position: int) -> None:
    """Moves the malt (antenna mast) to a specific position."""
    _LOGGER.info(f"Moving malt to position {position}.")
    verify_setting_mode(ctrl_axes_app, "Malt")
    ctrl_axes_app.set_target_position(position)
    ctrl_axes_app.click_btn_move_target_position()


def move_malt_to_step_position(ctrl_axes_app: "CtrlAxesDriver", step: int) -> None:
    """Moves the malt by a defined step increment."""
    _LOGGER.info(f"Moving malt by step: {step}.")
    verify_setting_mode(ctrl_axes_app, "Malt")
    ctrl_axes_app.set_step_position(step)
    ctrl_axes_app.click_btn_move_step_position()


def move_malt_to_minimum_position(ctrl_axes_app: "CtrlAxesDriver") -> None:
    """Moves the malt to its minimum position."""
    _LOGGER.info("Moving malt to minimum position.")
    verify_setting_mode(ctrl_axes_app, "Malt")
    ctrl_axes_app.move_to_min()


def move_malt_to_maximum_position(ctrl_axes_app: "CtrlAxesDriver") -> None:
    """Moves the malt to its maximum position."""
    _LOGGER.info("Moving malt to maximum position.")
    verify_setting_mode(ctrl_axes_app, "Malt")
    ctrl_axes_app.move_to_max()


def move_malt_to_horizontal_polar(ctrl_axes_app: "CtrlAxesDriver") -> None:
    """Sets the malt polarization to Horizontal."""
    _LOGGER.info("Setting malt polarization to Horizontal.")
    verify_setting_mode(ctrl_axes_app, "Malt")
    ctrl_axes_app.set_malt_orientation(horizontal=True)


def move_malt_to_vertical_polar(ctrl_axes_app: "CtrlAxesDriver") -> None:
    """Sets the malt polarization to Vertical."""
    _LOGGER.info("Setting malt polarization to Vertical.")
    verify_setting_mode(ctrl_axes_app, "Malt")
    ctrl_axes_app.set_malt_orientation(horizontal=False)
