import pytest
from unittest.mock import patch, MagicMock
from drivers.ui.ctrl_axes import CtrlAxesDriver, CtrlAxesUi

@pytest.fixture
def ctrl_axes_driver():
    """
    Provides a mocked instance of CtrlAxesDriver for unit testing.
    Patches the base class __init__ and mocks all inherited methods.
    """
    with patch("drivers.ui.base.AppUiDriver.__init__", return_value=None):
        driver = CtrlAxesDriver()
        # Mock all methods from the base class that are used by the driver
        driver.set_edit_text = MagicMock()
        driver.click_button = MagicMock()
        driver.found_and_click_edit = MagicMock()
        driver.get_text_content = MagicMock()
        driver.get_edit_value = MagicMock()
        driver.move_to_min = MagicMock()
        driver.move_to_max = MagicMock()
        yield driver

def test_set_target_position(ctrl_axes_driver):
    """Verifies setting the target position calls the base set_edit_text method."""
    ctrl_axes_driver.set_target_position(180)
    ctrl_axes_driver.set_edit_text.assert_called_with(CtrlAxesUi.InputTargetPosition, "180")

def test_click_move_to_target(ctrl_axes_driver):
    """Verifies clicking the move button calls the base click_button method."""
    ctrl_axes_driver.click_btn_move_target_position()
    ctrl_axes_driver.click_button.assert_called_with(CtrlAxesUi.ButtonMoveToTarget)

def test_set_turntable_settings(ctrl_axes_driver):
    """Verifies switching to turntable settings calls the correct base method."""
    ctrl_axes_driver.set_turntable_settings()
    ctrl_axes_driver.found_and_click_edit.assert_called_with(CtrlAxesUi.EditLineTurntable)

def test_set_malt_orientation(ctrl_axes_driver):
    """Verifies setting the malt orientation calls the correct base method."""
    ctrl_axes_driver.set_malt_orientation(horizontal=True)
    ctrl_axes_driver.click_button.assert_called_with(CtrlAxesUi.ButtonHorizontalSet)
    
    ctrl_axes_driver.set_malt_orientation(horizontal=False)
    ctrl_axes_driver.click_button.assert_called_with(CtrlAxesUi.ButtonVerticalSet)

def test_get_current_settings(ctrl_axes_driver):
    """Verifies that get_current_settings correctly parses the mode from the title."""
    ctrl_axes_driver.get_text_content.return_value = "Settings: Turntable"
    mode = ctrl_axes_driver.get_current_settings()
    assert mode == "Turntable"
    ctrl_axes_driver.get_text_content.assert_called_with(element=CtrlAxesUi.GroupTittleSettings)

def test_get_turntable_degrees(ctrl_axes_driver):
    """Verifies reading the turntable position calls the correct base method."""
    ctrl_axes_driver.get_edit_value.return_value = "90.5"
    degrees = ctrl_axes_driver.get_turntable_degrees()
    assert degrees == 90.5
    ctrl_axes_driver.get_edit_value.assert_called_with(CtrlAxesUi.EditLineTurntable)
