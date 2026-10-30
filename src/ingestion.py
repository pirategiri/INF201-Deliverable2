"""Task 1: Reading log files and parsing them."""
import re
from pathlib import Path


def read_file(path : str) -> tuple[str, str]:
    """Read a log file. Try UTF-8 first, then fallback to Latin-1.
    """
    path = Path(path)
    raw = path.read_bytes()
    try:
        return raw.decode("utf-8"), "utf-8"
    except UnicodeDecodeError:
        # Latin-1 accepts every byte, so it must be the fallback, not the first try
        return raw.decode("iso-8859-1"), "iso-8859-1"


LINE_PATTERN = re.compile(
    r"\[(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] "
    r"\[(?P<register_id>\w+)\] "
    r"item=(?P<item>.+?) "
    r"price=(?P<price>\d+\.\d+) "
    r"(?P<currency>[A-Z]{3}) "
    r"\((?P<status>SUCCESS|REFUND|CANCELLED)\)"
)


def parse_log(text : str) -> list[dict]:
    """Return a list of dicts, one per valid sales line. Noise lines are skipped."""
    records = []
    for line in text.splitlines():
        match = LINE_PATTERN.fullmatch(line.strip())
        if match:
            record = match.groupdict()
            record["price"] = float(record["price"])
            records.append(record)
    return records