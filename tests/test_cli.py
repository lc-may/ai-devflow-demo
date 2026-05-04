from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC = REPO_ROOT / "src"

SAMPLE_LOG = "\n".join(
    [
        "[0001.230] INFO boot start",
        "[0001.500] WARN wifi reconnect",
        "[0002.000] ERROR hardfault pc=0x23001234",
        "",
    ]
)


def _run_cli(log_path: Path, *extra_args: str) -> subprocess.CompletedProcess[str]:
    env = {**os.environ, "PYTHONPATH": str(SRC)}
    return subprocess.run(
        [sys.executable, "-m", "uartlog.cli", str(log_path), *extra_args],
        cwd=str(REPO_ROOT),
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )


def test_cli_format_json_sample(tmp_path: Path) -> None:
    log_path = tmp_path / "sample.log"
    log_path.write_text(SAMPLE_LOG, encoding="utf-8")

    proc = _run_cli(log_path, "--format", "json")
    assert proc.returncode == 0, proc.stderr
    data = json.loads(proc.stdout)
    assert data["info"] == 1
    assert data["warn"] == 1
    assert data["error"] == 1
    assert data["first_ts"] == pytest.approx(1.23)
    assert data["last_ts"] == 2.0
    assert data["duration"] == pytest.approx(0.77)


def test_cli_default_text_format(tmp_path: Path) -> None:
    log_path = tmp_path / "sample.log"
    log_path.write_text(SAMPLE_LOG, encoding="utf-8")

    proc = _run_cli(log_path)
    assert proc.returncode == 0, proc.stderr
    assert "INFO: 1" in proc.stdout
    assert "WARN: 1" in proc.stdout
    assert "ERROR: 1" in proc.stdout
    assert "first_ts: 1.23" in proc.stdout
    assert "last_ts: 2.0" in proc.stdout
    assert "duration: 0.77" in proc.stdout


def test_cli_format_json_empty_log(tmp_path: Path) -> None:
    log_path = tmp_path / "empty.log"
    log_path.write_text("", encoding="utf-8")

    proc = _run_cli(log_path, "--format", "json")
    assert proc.returncode == 0, proc.stderr
    data = json.loads(proc.stdout)
    assert data["info"] == 0
    assert data["warn"] == 0
    assert data["error"] == 0
    assert data["first_ts"] is None
    assert data["last_ts"] is None
    assert data["duration"] is None


def test_cli_format_json_only_invalid_lines(tmp_path: Path) -> None:
    log_path = tmp_path / "bad.log"
    log_path.write_text("not a uart line\nanother bad line\n", encoding="utf-8")

    proc = _run_cli(log_path, "--format", "json")
    assert proc.returncode == 0, proc.stderr
    data = json.loads(proc.stdout)
    assert data["info"] == 0
    assert data["first_ts"] is None
