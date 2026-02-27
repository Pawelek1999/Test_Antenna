import math
def calculate_sensitivity(gen_val, freq, distance, wire_loss, ant_factor):
    """
    Oblicza czułość (sensitivity) w dBµV/m oraz µV/m.
    Wzór: db = genVal - wireLoss - 20*log10(distance) + 20*log10(freq) - antFactor + 75.01
    """
    if gen_val is None:
        return None, None

    try:
        # Konwersja na float i obsługa ewentualnych błędów
        val = float(gen_val)
        f = float(freq) if freq is not None else 0.0
        d = float(distance) if distance is not None else 0.0
        wl = float(wire_loss) if wire_loss is not None else 0.0
        af = float(ant_factor) if ant_factor is not None else 0.0

        if f <= 0 or d <= 0:
            return None, None

        # Obliczenia dB (freq w MHz, distance w metrach)
        db = val - wl - (20 * math.log10(d)) + (20 * math.log10(f)) - af + 75.01
        
        # Obliczenia uV
        uv = math.pow(10, db / 20)
        
        return db, uv
    except Exception:
        return None, None