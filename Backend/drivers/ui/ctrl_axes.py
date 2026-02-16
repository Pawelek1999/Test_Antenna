import logging
from enum import StrEnum
from dataclasses import dataclass

from drivers.ui.base import AppUiDriver, UiElement

_LOGGER = logging.getLogger("CtrlAxesDriver")


class AutomationId(StrEnum):
    InputTargetPosition = "1020"
    BtnMoveToTarget = "1021"
    InputStepPosition = "1028"
    BtnMoveToTargetStep = "1023"
    BtnMoveToMin = "1017"
    BtnMoveToMax = "1018"
    BtnStop = "1019"
    EditLineTurntable = "1014"
    EditLineMalt = "1014"  # Note: Same ID as Turntable, distinguished by name
    RadioBtnHorizontalSet = "1024"
    RadioBtnVerticalSet = "1025"
    GroupTitleSettings = "1022"


@dataclass(frozen=True)
class CtrlAxesUi:
    InputTargetPosition = UiElement(
        auto_id=AutomationId.InputTargetPosition, control_type="Edit"
    )
    InputStepPosition = UiElement(
        auto_id=AutomationId.InputStepPosition, control_type="Edit"
    )
    ButtonMoveToTarget = UiElement(
        auto_id=AutomationId.BtnMoveToTarget, control_type="Button"
    )
    ButtonMoveToTargetStep = UiElement(
        auto_id=AutomationId.BtnMoveToTargetStep, control_type="Button"
    )
    ButtonMoveToMinPosition = UiElement(
        auto_id=AutomationId.BtnMoveToMin, control_type="Button"
    )
    ButtonMoveToMaxPosition = UiElement(
        auto_id=AutomationId.BtnMoveToMax, control_type="Button"
    )
    ButtonStop = UiElement(auto_id=AutomationId.BtnStop, control_type="Button")
    ButtonHorizontalSet = UiElement(
        auto_id=AutomationId.RadioBtnHorizontalSet, control_type="Button"
    )
    ButtonVerticalSet = UiElement(
        auto_id=AutomationId.RadioBtnVerticalSet, control_type="Button"
    )
    EditLineTurntable = UiElement(
        auto_id=AutomationId.EditLineTurntable, control_type="Edit", name="Degres"
    )
    EditLineMalt = UiElement(
        auto_id=AutomationId.EditLineMalt, control_type="Edit", name="Height"
    )
    GroupTittleSettings = UiElement(
        auto_id=AutomationId.GroupTitleSettings, control_type="Group"
    )


class CtrlAxesDriver(AppUiDriver):
    """
    Specialized driver for controlling the Axes/Turntable UI application.
    """

    def click_button_stop(self) -> None:
        """Triggers the emergency stop button."""
        self.click_button(CtrlAxesUi.ButtonStop)

    def set_target_position(self, position: int) -> None:
        """Sets the target position value in the input field."""
        self.set_edit_text(CtrlAxesUi.InputTargetPosition, str(position))

    def click_btn_move_target_position(self) -> None:
        """Clicks the button to move to the specified target position."""
        self.click_button(CtrlAxesUi.ButtonMoveToTarget)

    def set_step_position(self, position: int) -> None:
        """Sets the step increment value."""
        self.set_edit_text(CtrlAxesUi.InputStepPosition, str(position))

    def click_btn_move_step_position(self) -> None:
        """Clicks the button to move by the defined step increment."""
        self.click_button(CtrlAxesUi.ButtonMoveToTargetStep)

    def set_turntable_settings(self) -> None:
        """Switches the settings context to 'Turntable'."""
        self.found_and_click_edit(CtrlAxesUi.EditLineTurntable)

    def set_malt_settings(self) -> None:
        """Switches the settings context to 'Malt'."""
        self.found_and_click_edit(CtrlAxesUi.EditLineMalt)

    def set_malt_orientation(self, horizontal: bool = True) -> None:
        """
        Sets the malt orientation (Horizontal/Vertical).
        This should be called after switching to the 'Malt' settings mode.
        """
        target = (
            CtrlAxesUi.ButtonHorizontalSet
            if horizontal
            else CtrlAxesUi.ButtonVerticalSet
        )
        _LOGGER.debug(
            "Setting malt orientation to: %s",
            "Horizontal" if horizontal else "Vertical",
        )
        self.click_button(target)

    def get_current_settings(self) -> str:
        """
        Reads the current settings mode from the group title.
        Example: "Settings: Turntable" -> "Turntable"
        """
        return (
            self.get_text_content(element=CtrlAxesUi.GroupTittleSettings)
            .split(":")[-1]
            .strip()
        )

    def get_turntable_degrees(self) -> float:
        """Reads the current turntable position in degrees."""
        return float(self.get_edit_value(CtrlAxesUi.EditLineTurntable))

    def get_malt_height(self) -> float:
        """Reads the current malt height."""
        return float(self.get_edit_value(CtrlAxesUi.EditLineMalt))

    def move_to_min(self) -> None:
        """Commands movement to the minimum position."""
        self.click_button(CtrlAxesUi.ButtonMoveToMinPosition)

    def move_to_max(self) -> None:
        """Commands movement to the maximum position."""
        self.click_button(CtrlAxesUi.ButtonMoveToMaxPosition)


if __name__ == "__main__":
    APP_EXE = "C:\\AcEmcV7\\CtrlAxesV7.exe"
    APP_NAME = r"Somfy_Pologne\.cmp - CtrlAxesV7.*"
    ctrl_axes_inst = CtrlAxesDriver()
    ctrl_axes_inst.start_or_attach(app_name=APP_NAME, app_exe=APP_EXE)

    position = ctrl_axes_inst.get_turntable_degrees()
    print(position)
