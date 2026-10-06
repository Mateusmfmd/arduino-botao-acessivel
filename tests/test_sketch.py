from pathlib import Path


SKETCH = Path(__file__).parents[1] / "arduino-botao-acessivel.ino"


def test_sketch_has_expected_pin_and_debounce_configuration():
    source = SKETCH.read_text(encoding="utf-8")
    assert "const byte PINO_BOTAO = 2;" in source
    assert "INPUT_PULLUP" in source
    assert "TEMPO_DEBOUNCE_MS = 35" in source
    assert "millis()" in source


def test_serial_protocol_is_documented_in_firmware():
    source = SKETCH.read_text(encoding="utf-8")
    assert "BOTAO_ACESSIVEL:PRONTO" in source
    assert "PRESSIONADO" in source
    assert "SOLTO" in source


def test_button_events_are_emitted_only_after_stable_state_change():
    source = SKETCH.read_text(encoding="utf-8")
    assert "leituraEstavel != leituraAtual" in source
    assert "emitirEvento(pressionado" in source
