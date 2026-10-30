"""Task 2: recursive Function """
from pathlib import Path


def find_log_files(folder):
    """Return a list of Path objects for all .log files in folder and its subfolders."""
    folder = Path(folder)
    found = []
    for item in folder.iterdir():
        if item.is_dir():
            found.extend(find_log_files(item))  # go deeper
        elif item.is_file() and item.suffix == ".log":
            found.append(item)
    return found


def find_active_registers(data):
    """Return the set of register ids where "active" is true.

    Works on any mix of nested dicts and lists.
    """
    active = set()
    if isinstance(data, dict):
        if data.get("active") is True and "id" in data:
            active.add(data["id"])
        for value in data.values():
            active |= find_active_registers(value)
    elif isinstance(data, list):
        for element in data:
            active |= find_active_registers(element)
    return active