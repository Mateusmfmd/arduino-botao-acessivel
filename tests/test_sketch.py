from pathlib import Path
import subprocess


ROOT = Path(__file__).parents[1]
SKETCH = ROOT / "arduino-botao-acessivel.ino"
README = ROOT / "README.md"
WORKFLOW = ROOT / ".github" / "workflows" / "ci.yml"
LICENSE = ROOT / "LICENSE"
GITIGNORE = ROOT / ".gitignore"


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


def test_project_documentation_and_license_are_present_in_portuguese():
    readme = README.read_text(encoding="utf-8")
    assert "## Como executar" in readme
    assert "## Validação local" in readme
    assert "## Licença" in readme
    assert "[LICENSE](LICENSE)" in readme
    assert LICENSE.read_text(encoding="utf-8").startswith("MIT License")


def test_ci_runs_structural_tests_and_arduino_compilation():
    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert "pytest -q" in workflow
    assert "arduino-cli compile --fqbn arduino:avr:uno ." in workflow


def test_no_cache_or_build_artifact_is_tracked():
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    tracked = result.stdout.splitlines()
    forbidden_fragments = (
        "/__pycache__/",
        "/.pytest_cache/",
        "/.mypy_cache/",
        "/.ruff_cache/",
        "/.cache/",
        "/.arduino15/",
        "/build/",
        "/dist/",
    )
    forbidden_suffixes = (".pyc", ".pyo", ".hex", ".elf", ".map", ".bin")
    assert not any(
        any(f"/{fragment.strip('/')}/" in f"/{path}" for fragment in forbidden_fragments)
        or path.endswith(forbidden_suffixes)
        for path in tracked
    )


def test_gitignore_covers_common_local_caches_and_artifacts():
    gitignore = GITIGNORE.read_text(encoding="utf-8")
    for entry in ("__pycache__/", ".pytest_cache/", ".arduino15/", "build/", "*.hex"):
        assert entry in gitignore
