import pytest
from unittest.mock import patch, MagicMock
from drivers.ui.calculator import CalculatorDriver, CalculatorUi

@pytest.fixture
def calculator_driver():
    """
    Provides a mocked instance of CalculatorDriver for unit testing.
    This fixture patches the base class's __init__ to prevent it from
    running and then mocks the inherited methods.
    """
    with patch("drivers.ui.base.AppUiDriver.__init__", return_value=None):
        driver = CalculatorDriver()
        driver.click_button = MagicMock()
        driver.get_text_content = MagicMock()
        yield driver

def test_enter_number(calculator_driver):
    """Verifies that enter_number clicks the correct sequence of buttons."""
    calculator_driver.enter_number(123)
    
    assert calculator_driver.click_button.call_count == 3
    calculator_driver.click_button.assert_any_call(CalculatorUi.BtnNb1)
    calculator_driver.click_button.assert_any_call(CalculatorUi.BtnNb2)
    calculator_driver.click_button.assert_any_call(CalculatorUi.BtnNb3)

def test_operations(calculator_driver):
    """Verifies that arithmetic operation methods call the base click_button method."""
    calculator_driver.click_plus()
    calculator_driver.click_button.assert_called_with(CalculatorUi.BtnPlus)
    
    calculator_driver.click_minus()
    calculator_driver.click_button.assert_called_with(CalculatorUi.BtnMinus)
    
    calculator_driver.click_multiply()
    calculator_driver.click_button.assert_called_with(CalculatorUi.BtnMultiply)
    
    calculator_driver.click_divide()
    calculator_driver.click_button.assert_called_with(CalculatorUi.BtnDivide)
    
    calculator_driver.click_equal()
    calculator_driver.click_button.assert_called_with(CalculatorUi.BtnEqual)
    
    calculator_driver.click_clear()
    calculator_driver.click_button.assert_called_with(CalculatorUi.BtnClear)

def test_get_result(calculator_driver):
    """Verifies that get_result correctly parses the raw text from the display."""
    calculator_driver.get_text_content.return_value = "Display is 42"
    
    result = calculator_driver.get_result()
    
    assert result == "42"
    calculator_driver.get_text_content.assert_called_with(CalculatorUi.OutputWindow)

def test_enter_number_with_invalid_char(calculator_driver):
    """Verifies that non-digit characters in the input are ignored."""
    calculator_driver.enter_number("1a2b")
    
    assert calculator_driver.click_button.call_count == 2
    calculator_driver.click_button.assert_any_call(CalculatorUi.BtnNb1)
    calculator_driver.click_button.assert_any_call(CalculatorUi.BtnNb2)
