from __future__ import annotations

import argparse
from pathlib import Path

from uartlog.parser import summarize


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze MCU UART log files")
    parser.add_argument("log_file", type=Path, help="Path to UART log file")
    args = parser.parse_args()

    lines = args.log_file.read_text(encoding="utf-8").splitlines()
    result = summarize(lines)

    print(f"INFO: {result.info}")
    print(f"WARN: {result.warn}")
    print(f"ERROR: {result.error}")
    print(f"first_ts: {result.first_ts}")
    print(f"last_ts: {result.last_ts}")
    print(f"duration: {result.duration}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
