import os
import time
import tarfile
from datetime import datetime


# ── Config ────────────────────────────────────────────────────────────────────

SCHEDULES_FILE = "backup_schedules.txt"
LOG_FILE = os.path.join("logs", "backup_service.log")
BACKUPS_DIR = "backups"
SLEEP_SECONDS = 45


# ── Helpers ───────────────────────────────────────────────────────────────────

def timestamp():
    """Return current time as [dd/mm/yyyy hh:mm]."""
    return datetime.now().strftime("[%d/%m/%Y %H:%M]")


def log(message):
    """Append a timestamped message to the service log file."""
    os.makedirs("logs", exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp()} {message}\n")


# ── Core Logic ────────────────────────────────────────────────────────────────

def read_schedules():
    """Read and return list of schedule strings from the file."""
    try:
        with open(SCHEDULES_FILE, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []


def write_schedules(schedules):
    """Overwrite the schedules file with the given list."""
    with open(SCHEDULES_FILE, "w") as f:
        f.write("\n".join(schedules) + ("\n" if schedules else ""))


def make_backup(source_path, backup_name):
    """Create a compressed .tar archive of source_path in the backups dir."""
    os.makedirs(BACKUPS_DIR, exist_ok=True)
    tar_path = os.path.join(BACKUPS_DIR, f"{backup_name}.tar")

    with tarfile.open(tar_path, "w") as tar:
        tar.add(source_path, arcname=os.path.basename(source_path))

    return tar_path


def process_schedules():
    """
    Check each schedule against the current time.
    Perform a backup for matching schedules and remove them from the file.
    """
    now = datetime.now()
    current_hhmm = now.strftime("%H:%M")

    schedules = read_schedules()
    remaining = []

    for entry in schedules:
        parts = entry.split(";")
        if len(parts) != 3:
            log(f"Error: malformed schedule skipped: {entry}")
            remaining.append(entry)
            continue

        source_path, sched_time, backup_name = [p.strip() for p in parts]

        if sched_time == current_hhmm:
            try:
                tar_path = make_backup(source_path, backup_name)
                log(f"Backup done for {source_path} in {tar_path}")
            except Exception as e:
                log(f"Error: backup failed for {source_path}: {e}")
                remaining.append(entry)  
        else:
            remaining.append(entry)

    write_schedules(remaining)


# ── Main Loop ─────────────────────────────────────────────────────────────────

def main():
    log("backup_service started")
    while True:
        try:
            process_schedules()
        except Exception as e:
            log(f"Error: unexpected error in service loop: {e}")
        time.sleep(SLEEP_SECONDS)


if __name__ == "__main__":
    main()