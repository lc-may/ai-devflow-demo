from __future__ import annotations

from dataclasses import dataclass
import re


LOG_RE = re.compile(
    r"^\[(?P<ts>\d+\.\d+)\]\s+(?P<level>INFO|WARN|ERROR)\s+(?P<message>.*)$"
)


@dataclass(frozen=True)
class LogEntry:
    timestamp: float
    level: str
    message: str


@dataclass(frozen=True)
class LogSummary:
    info: int
    warn: int
    error: int
    first_ts: float | None
    last_ts: float | None
    duration: float | None


def parse_line(line: str) -> LogEntry | None:
    """Parse one UART log line."""
    match = LOG_RE.match(line.strip())
    if not match:
        return None

    return LogEntry(
        timestamp=float(match.group("ts")),
        level=match.group("level"),
        message=match.group("message"),
    )


def summarize(lines: list[str]) -> LogSummary:
    entries = [entry for line in lines if (entry := parse_line(line)) is not None]

    if not entries:
        return LogSummary(
            info=0,
            warn=0,
            error=0,
            first_ts=None,
            last_ts=None,
            duration=None,
        )

    first_ts = entries[0].timestamp
    last_ts = entries[-1].timestamp

    return LogSummary(
        info=sum(1 for e in entries if e.level == "INFO"),
        warn=sum(1 for e in entries if e.level == "WARN"),
        error=sum(1 for e in entries if e.level == "ERROR"),
        first_ts=first_ts,
        last_ts=last_ts,
        duration=last_ts - first_ts,
    )
