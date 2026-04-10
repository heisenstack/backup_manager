import sys
import os
import subprocess
from datetime import datetime


# ── Helpers ──────────────────────────────────────────────────────────────────

SCHEDULES_FILE = "backup_schedules.txt"
LOG_FILE = os.path.join("logs", "backup_manager.log")
BACKUPS_DIR = "backups"
SERVICE_SCRIPT = "backup_service.py"


def timestamp():
    """Return current time as [dd/mm/yyyy hh:mm]."""
    return datetime.now().strftime("[%d/%m/%Y %H:%M]")


def log(message):
    """Append a timestamped message to the manager log file."""
    os.makedirs("logs", exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp()} {message}\n")
    print(f"{timestamp()} {message}")


# ── Commands ──────────────────────────────────────────────────────────────────

def cmd_create(schedule):
    """Add a new schedule line to backup_schedules.txt."""
    parts = schedule.split(";")
    if len(parts) != 3 or any(p.strip() == "" for p in parts):
        log(f"Error: malformed schedule: {schedule}")
        return

    _, time_str, name = parts
    time_parts = time_str.strip().split(":")
    if len(time_parts) != 2 or not all(p.isdigit() for p in time_parts):
        log(f"Error: malformed schedule: {schedule}")
        return

    try:
        with open(SCHEDULES_FILE, "a") as f:
            f.write(schedule.strip() + "\n")
        log(f"New schedule added: {schedule.strip()}")
    except Exception as e:
        log(f"Error: could not write schedule: {e}")


def cmd_list():
    """Print all schedules with their index."""
    log("Show schedules list")
    try:
        with open(SCHEDULES_FILE, "r") as f:
            lines = [l.strip() for l in f if l.strip()]
        if not lines:
            print("(no schedules)")
        for i, line in enumerate(lines):
            print(f"{i}: {line}")
    except FileNotFoundError:
        log("Error: can't find backup_schedules.txt")


def cmd_delete(index_str):
    """Delete the schedule at the given index."""
    try:
        index = int(index_str)
    except ValueError:
        log(f"Error: invalid index: {index_str}")
        return

    try:
        with open(SCHEDULES_FILE, "r") as f:
            lines = [l.strip() for l in f if l.strip()]
    except FileNotFoundError:
        log("Error: can't find backup_schedules.txt")
        return

    if index < 0 or index >= len(lines):
        log(f"Error: can't find schedule at index {index}")
        return

    lines.pop(index)
    with open(SCHEDULES_FILE, "w") as f:
        f.write("\n".join(lines) + ("\n" if lines else ""))
    log(f"Schedule at index {index} deleted")


def cmd_start():
    """Launch backup_service.py as a background process."""
    try:
        result = subprocess.run(
            ["pgrep", "-f", SERVICE_SCRIPT],
            capture_output=True, text=True
        )
        if result.stdout.strip():
            log("Error: backup_service already running")
            return
    except Exception:
        pass  

    try:
        subprocess.Popen(
            [sys.executable, SERVICE_SCRIPT],
            start_new_session=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        log("backup_service started")
    except Exception as e:
        log(f"Error: could not start backup_service: {e}")


def cmd_stop():
    """Kill the running backup_service.py process."""
    try:
        result = subprocess.run(
            ["pgrep", "-f", SERVICE_SCRIPT],
            capture_output=True, text=True
        )
        pids = result.stdout.strip().splitlines()
        if not pids:
            log("Error: can't stop backup_service")
            return
        for pid in pids:
            os.kill(int(pid), 15) 
        log("backup_service stopped")
    except Exception as e:
        log(f"Error: can't stop backup_service: {e}")


def cmd_backups():
    """List all .tar files in the backups directory."""
    log("Show backups list")
    # if not os.path.exists(BACKUPS_DIR):
    #     log("Error: can't find backups directory")
    #     return
    # os.makedirs(BACKUPS_DIR, exist_ok=True)
    try:
        files = os.listdir(BACKUPS_DIR)
        tar_files = [f for f in files if f.endswith(".tar")]
        if not tar_files:
            print("(no backups)")
        for f in tar_files:
            print(f)
    except FileNotFoundError:
        log("Error: can't find backups directory")


# ── Entry Point ───────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        log("Error: no command provided")
        print("Usage: python3 backup_manager.py <command> [args]")
        return

    command = sys.argv[1]

    if command == "create":
        if len(sys.argv) < 3:
            log("Error: missing schedule argument for create")
        else:
            cmd_create(sys.argv[2])

    elif command == "list":
        cmd_list()

    elif command == "delete":
        if len(sys.argv) < 3:
            log("Error: missing index argument for delete")
        else:
            cmd_delete(sys.argv[2])

    elif command == "start":
        cmd_start()

    elif command == "stop":
        cmd_stop()

    elif command == "backups":
        cmd_backups()

    else:
        log(f"Error: unknown command: {command}")


if __name__ == "__main__":
    main()