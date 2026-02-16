import enum
import logging
from dataclasses import dataclass
from drivers.ui.base import AppUiDriver, UiElement

_LOGGER = logging.getLogger(__name__)


class ControlType(enum.StrEnum):
    Button = "Button"
    Text = "Text"


class AutomationId(enum.StrEnum):
    equalButton = "equalButton"
    plusButton = "plusButton"
    minusButton = "minusButton"
    multiplyButton = "multiplyButton"
    divideButton = "divideButton"
    clearButton = "clearButton"

    num0Button = "num0Button"
    num1Button = "num1Button"
    num2Button = "num2Button"
    num3Button = "num3Button"
    num4Button = "num4Button"
    num5Button = "num5Button"
    num6Button = "num6Button"
    num7Button = "num7Button"
    num8Button = "num8Button"
    num9Button = "num9Button"

    CalculatorResults = "CalculatorResults"


@dataclass(frozen=True)
class CalculatorUi:
    OutputWindow = UiElement(auto_id=AutomationId.CalculatorResults, control_type=ControlType.Text)
    BtnEqual = UiElement(auto_id=AutomationId.equalButton, control_type=ControlType.Button)
    BtnPlus = UiElement(auto_id=AutomationId.plusButton, control_type=ControlType.Button)
    BtnMinus = UiElement(auto_id=AutomationId.minusButton, control_type=ControlType.Button)
    BtnMultiply = UiElement(auto_id=AutomationId.multiplyButton, control_type=ControlType.Button)
    BtnDivide = UiElement(auto_id=AutomationId.divideButton, control_type=ControlType.Button)
    BtnClear = UiElement(auto_id=AutomationId.clearButton, control_type=ControlType.Button)

    BtnNb0 = UiElement(auto_id=AutomationId.num0Button, control_type=ControlType.Button)
    BtnNb1 = UiElement(auto_id=AutomationId.num1Button, control_type=ControlType.Button)
    BtnNb2 = UiElement(auto_id=AutomationId.num2Button, control_type=ControlType.Button)
    BtnNb3 = UiElement(auto_id=AutomationId.num3Button, control_type=ControlType.Button)
    BtnNb4 = UiElement(auto_id=AutomationId.num4Button, control_type=ControlType.Button)
    BtnNb5 = UiElement(auto_id=AutomationId.num5Button, control_type=ControlType.Button)
    BtnNb6 = UiElement(auto_id=AutomationId.num6Button, control_type=ControlType.Button)
    BtnNb7 = UiElement(auto_id=AutomationId.num7Button, control_type=ControlType.Button)
    BtnNb8 = UiElement(auto_id=AutomationId.num8Button, control_type=ControlType.Button)
    BtnNb9 = UiElement(auto_id=AutomationId.num9Button, control_type=ControlType.Button)


class CalculatorDriver(AppUiDriver):
    """Driver for the Windows Calculator application."""

    def __init__(self):
        self._num_buttons = {
            '0': CalculatorUi.BtnNb0, '1': CalculatorUi.BtnNb1, '2': CalculatorUi.BtnNb2,
            '3': CalculatorUi.BtnNb3, '4': CalculatorUi.BtnNb4, '5': CalculatorUi.BtnNb5,
            '6': CalculatorUi.BtnNb6, '7': CalculatorUi.BtnNb7, '8': CalculatorUi.BtnNb8,
            '9': CalculatorUi.BtnNb9
        }
        super().__init__()

    def get_result(self) -> str:
        """Retrieves and parses the result from the calculator display."""
        raw_text = self.get_text_content(CalculatorUi.OutputWindow)
        # Example: "Display is 5" -> "5"
        result = raw_text.replace("Display is", "").strip()
        _LOGGER.debug(f"Parsed result: '{result}' (Raw: '{raw_text}')")
        return result

    def enter_number(self, number: int | str) -> None:
        """Enters a number by clicking the corresponding digit buttons."""
        _LOGGER.info(f"Entering number: {number}")
        for digit in str(number):
            if digit in self._num_buttons:
                self.click_button(self._num_buttons[digit])
            else:
                _LOGGER.warning(f"Character '{digit}' is not a clickable digit.")

    def click_plus(self):
        self.click_button(CalculatorUi.BtnPlus)

    def click_minus(self):
        self.click_button(CalculatorUi.BtnMinus)

    def click_multiply(self):
        self.click_button(CalculatorUi.BtnMultiply)

    def click_divide(self):
        self.click_button(CalculatorUi.BtnDivide)

    def click_equal(self):
        self.click_button(CalculatorUi.BtnEqual)

    def click_clear(self):
        self.click_button(CalculatorUi.BtnClear)
