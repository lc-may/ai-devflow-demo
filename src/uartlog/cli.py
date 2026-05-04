from __future__ import annotations

import argparse
import json
from pathlib import Path

from uartlog.parser import LogSummary, summarize


def _summary_to_json_dict(summary: LogSummary) -> dict[str, object]:
    return {
        "info": summary.info,
        "warn": summary.warn,
        "error": summary.error,
        "first_ts": summary.first_ts,
        "last_ts": summary.last_ts,
        "duration": summary.duration,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze MCU UART log files")
    parser.add_argument("log_file", type=Path, help="Path to UART log file")
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format (default: text)",
    )
    args = parser.parse_args()

    lines = args.log_file.read_text(encoding="utf-8").splitlines()
    result = summarize(lines)

    if args.format == "json":
        print(json.dumps(_summary_to_json_dict(result), indent=2))
    else:
        print(f"INFO: {result.info}")
        print(f"WARN: {result.warn}")
        print(f"ERROR: {result.error}")
        print(f"first_ts: {result.first_ts}")
        print(f"last_ts: {result.last_ts}")
        print(f"duration: {result.duration}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
