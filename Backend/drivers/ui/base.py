import re
import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional, Union, Any
from pywinauto import Application, WindowSpecification

if TYPE_CHECKING:
    from pywinauto.controls.uia_controls import (
        ButtonWrapper,
        EditWrapper,
        StaticWrapper,
    )

_LOGGER = logging.getLogger("AppUiDriver")


@dataclass(frozen=True)
class UiElement:
    """
    Represents metadata for a UI control.

    Attributes:
        auto_id: The AutomationId of the control.
        control_type: The UIA control type (e.g., 'Button', 'Edit').
        name: An optional friendly name for logging and disambiguation.
    """

    auto_id: Union[str, Any]
    control_type: str
    name: Optional[str] = None


class AppUiDriver:
    """
    Generic UIA application driver providing a high-level API for UI automation.
    This driver encapsulates pywinauto's UIA backend.
    """

    def __init__(self):
        """Initializes the driver with the UIA backend."""
        self.app: Application = Application(backend="uia")
        self.win: Optional[WindowSpecification] = None
        _LOGGER.debug("Driver initialized with UIA backend.")

    def start_or_attach(self, app_name: str, app_exe: str) -> None:
        """
        Connects to a running application or starts a new one.

        Args:
            app_name: A regular expression for the application window title.
            app_exe: The full path to the application executable.
        """
        _LOGGER.info(f"Attempting to start or attach to: {app_name}")
        try:
            self.app.connect(path=app_exe, timeout=20)
            _LOGGER.info("Successfully attached to running instance by path.")
        except Exception:
            _LOGGER.warning("Could not attach by path, trying by title...")
            try:
                self.app.connect(title_re=app_name, timeout=20)
                _LOGGER.info("Successfully attached to running instance by title.")
            except Exception:
                _LOGGER.info(f"Application not found. Starting new instance: {app_exe}")
                self.app.start(app_exe)
                self.app.connect(title_re=app_name, timeout=20)

        self.win = self.app.window(title_re=app_name)
        self.win.wait("ready", timeout=20)
        _LOGGER.info("Main window focused and ready.")

    def click_button(self, element: UiElement, is_radio_btn: bool = False) -> None:
        """
        Clicks a button or selects a radio button.

        Args:
            element: The UiElement definition of the control.
            is_radio_btn: If True, treats the element as a RadioButton and uses .select().
        """
        action = "Selecting radio" if is_radio_btn else "Clicking button"
        _LOGGER.debug(f"{action}: {element.name or element.auto_id}")
        btn = self._get_button_wrapper(element)
        if is_radio_btn:
            btn.select()
        else:
            btn.click_input()

    def check_state_button(self, element: UiElement) -> bool:
        """
        Checks if a button (e.g., ToggleButton, RadioButton) is selected.

        Args:
            element: The UiElement definition.
        Returns:
            True if the control is selected, False otherwise.
        """
        btn = self._get_button_wrapper(element)
        return btn.is_selected()

    def set_edit_text(self, element: UiElement, value: str) -> None:
        """
        Sets the text content of an edit field.

        Args:
            element: The UiElement definition of the edit field.
            value: The string value to set.
        """
        _LOGGER.debug(
            f"Setting text in '{element.name or element.auto_id}' to '{value}'"
        )
        edit = self._get_edit_wrapper(element)
        edit.set_text(value)

    def get_edit_value(self, element: UiElement) -> str:
        """Retrieves the value from an edit field."""
        return self._get_edit_wrapper(element).get_value()

    def found_and_click_edit(self, element: UiElement) -> None:
        """Sets focus to and clicks an edit field."""
        edit = self._get_edit_wrapper(element=element)
        edit.set_focus()
        edit.click_input()

    def get_text_content(self, element: UiElement) -> str:
        """
        Retrieves the text content from a control (e.g., Edit, Text).

        Args:
            element: The UiElement definition.
        Returns:
            The text content of the control.
        """
        _LOGGER.debug(f"Getting text from: {element.name or element.auto_id}")
        wrapper = self._get_wrapper(element)
        return wrapper.window_text()

    def _get_wrapper(self, element: UiElement) -> Any:
        """
        Resolves a UiElement to its pywinauto wrapper object.

        Args:
            element: The UiElement metadata to find.
        Returns:
            The pywinauto wrapper object.
        Raises:
            RuntimeError: If the control is not found or its type mismatches.
        """
        self._ensure_visible()
        expected_type = element.control_type.capitalize()
        search_params = {"auto_id": str(element.auto_id), "control_type": expected_type}
        if element.name:
            search_params["title"] = element.name

        _LOGGER.debug(f"Searching for element with params: {search_params}")
        spec = self.win.child_window(**search_params)

        try:
            spec.wait("exists", timeout=5)
            wrapper = spec.wrapper_object()
            if wrapper.element_info.control_type != expected_type:
                raise RuntimeError(
                    f"Type mismatch for ID '{element.auto_id}'. "
                    f"Expected: {expected_type}, Got: {wrapper.element_info.control_type}"
                )
            return wrapper
        except Exception as e:
            _LOGGER.error(
                f"Failed to retrieve {element.auto_id} ({expected_type}): {e}"
            )
            raise RuntimeError(
                f"Control '{element.auto_id}' not found or type mismatch."
            ) from e

    def _get_button_wrapper(self, element: UiElement) -> "ButtonWrapper":
        """Helper to get a type-hinted ButtonWrapper."""
        return self._get_wrapper(element)

    def _get_edit_wrapper(self, element: UiElement) -> "EditWrapper":
        """Helper to get a type-hinted EditWrapper."""
        return self._get_wrapper(element)

    def _get_text_wrapper(self, element: UiElement) -> "StaticWrapper":
        """Helper to get a type-hinted StaticWrapper."""
        return self._get_wrapper(element)

    def _ensure_visible(self) -> None:
        """Ensures the main window is available and focused."""
        if self.win is None:
            raise RuntimeError("Driver not initialized. Call start_or_attach() first.")
        if self.win.is_minimized():
            self.win.restore()
        self.win.set_focus()
