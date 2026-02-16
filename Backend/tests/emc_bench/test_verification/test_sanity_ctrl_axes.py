import pytest
import logging

_LOGGER = logging.getLogger("Test.Sanity.CtrlAxes")


@pytest.mark.hardware
class TestCtrlAxesSanity:
    """
    Sanity checks for the CtrlAxes UI application.
    """

    def test_connection_and_initial_state(self, ctrl_axes):
        """
        Verifies:
        1. Successful connection to the CtrlAxes application.
        2. The ability to read the initial turntable position.
        """
        _LOGGER.info("--- Verifying CtrlAxes Connection and Initial State ---")

        # The fixture 'ctrl_axes' already handles the connection.
        # If it fails, the test will fail during setup.
        _LOGGER.info("Successfully connected to the CtrlAxes application.")

        initial_pos = ctrl_axes.get_turntable_degrees()
        ctrl_axes.set_turntable_settings()
        ctrl_axes.set_target_position(30)
        ctrl_axes.click_btn_move_target_position()
        _LOGGER.info(f"Initial turntable position: {initial_pos}")

        assert isinstance(
            initial_pos, float
        ), "Could not read a valid float for the initial position."
