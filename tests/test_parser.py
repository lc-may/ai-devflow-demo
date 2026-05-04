from uartlog.parser import parse_line, summarize


def test_parse_valid_line() -> None:
    entry = parse_line("[0001.230] INFO boot start")

    assert entry is not None
    assert entry.timestamp == 1.230
    assert entry.level == "INFO"
    assert entry.message == "boot start"


def test_parse_invalid_line() -> None:
    entry = parse_line("invalid line")

    assert entry is None


def test_summarize() -> None:
    lines = [
        "[0001.230] INFO boot start",
        "[0001.500] WARN wifi reconnect",
        "[0002.000] ERROR hardfault pc=0x23001234",
    ]

    summary = summarize(lines)

    assert summary.info == 1
    assert summary.warn == 1
    assert summary.error == 1
    assert summary.first_ts == 1.230
    assert summary.last_ts == 2.000
    assert round(summary.duration or 0, 3) == 0.770
