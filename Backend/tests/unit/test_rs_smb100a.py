import pytest
from unittest.mock import MagicMock, patch, call
from drivers.rs_smb100a import SMB100A, InstrumentRangeError, InstrumentConnectionError

# Adres testowy (nie ma znaczenia przy mockowaniu)
RESOURCE = "TCPIP::1.2.3.4::INSTR"

@pytest.fixture
def mock_rs_inst():
    """Mockuje klase RsInstrument z biblioteki zewnetrznej."""
    with patch("drivers.rs_smb100a.RsInstrument") as MockClass:
        # Instancja zwracana przez konstruktor
        mock_instance = MockClass.return_value
        yield mock_instance

def test_init_connection_success(mock_rs_inst):
    """Sprawdza czy sterownik poprawnie inicjalizuje polaczenie."""
    driver = SMB100A(RESOURCE)
    
    # Sprawdz czy RsInstrument zostal wywolany z dobrym adresem
    mock_rs_inst.assert_not_called() # To jest instancja, sprawdzamy klase w patchu wyzej, 
                                     # ale tutaj sprawdzamy czy timeout zostal ustawiony
    assert driver.inst == mock_rs_inst
    assert driver.inst.visa_timeout == 5000

def test_init_connection_failure():
    """Sprawdza czy rzucany jest wyjatek gdy nie mozna sie polaczyc."""
    with patch("drivers.rs_smb100a.RsInstrument", side_effect=Exception("Connection refused")):
        with pytest.raises(InstrumentConnectionError):
            SMB100A(RESOURCE)

def test_set_frequency_valid(mock_rs_inst):
    """Sprawdza wysylanie komendy ustawienia czestotliwosci."""
    driver = SMB100A(RESOURCE)
    driver.set_frequency(1000.50)
    
    # Oczekujemy formatowania do 2 miejsc po przecinku
    driver.inst.write_with_opc.assert_called_with("FREQ 1000.50")

def test_set_frequency_invalid(mock_rs_inst):
    """Sprawdza walidacje zakresu czestotliwosci."""
    driver = SMB100A(RESOURCE)
    with pytest.raises(InstrumentRangeError):
        driver.set_frequency(-100)
    
    # Upewnij sie ze nic nie wyslano
    driver.inst.write_with_opc.assert_not_called()

def test_get_frequency(mock_rs_inst):
    """Sprawdza odczyt czestotliwosci."""
    driver = SMB100A(RESOURCE)
    mock_rs_inst.query_float_with_opc.return_value = 868.0
    
    freq = driver.get_frequency()
    
    assert freq == 868.0
    driver.inst.query_float_with_opc.assert_called_with("FREQ?")

def test_set_power_valid(mock_rs_inst):
    """Sprawdza ustawianie mocy."""
    driver = SMB100A(RESOURCE)
    driver.set_power(-50.5)
    driver.inst.write_with_opc.assert_called_with("POW -50.50")

def test_set_power_out_of_range(mock_rs_inst):
    """Sprawdza walidacje zakresu mocy."""
    driver = SMB100A(RESOURCE)
    with pytest.raises(InstrumentRangeError):
        driver.set_power(30) # Max is 20
    with pytest.raises(InstrumentRangeError):
        driver.set_power(-130) # Min is -120

def test_rf_output(mock_rs_inst):
    """Sprawdza wlaczanie i wylaczanie RF."""
    driver = SMB100A(RESOURCE)
    
    driver.set_output_rf(True)
    driver.inst.write_with_opc.assert_called_with("OUTP ON")
    
    driver.set_output_rf(False)
    driver.inst.write_with_opc.assert_called_with("OUTP OFF")

def test_safe_state(mock_rs_inst):
    """Sprawdza czy safe_state ustawia bezpieczne parametry."""
    driver = SMB100A(RESOURCE)
    driver.safe_state()
    
    # Oczekujemy wylaczenia RF i ustawienia minimalnej mocy
    expected_calls = [
        call("OUTP OFF"),
        call("POW -120.00")
    ]
    driver.inst.write_with_opc.assert_has_calls(expected_calls, any_order=True)

def test_context_manager(mock_rs_inst):
    """Sprawdza czy 'with' poprawnie zamyka polaczenie i ustawia safe state."""
    with SMB100A(RESOURCE) as driver:
        pass
    
    # Po wyjsciu z with powinno byc safe_state i close
    assert driver.inst.write_with_opc.call_count >= 2 # safe state calls
    driver.inst.close.assert_called_once()
