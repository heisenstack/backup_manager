import os
import sys
from datetime import datetime
import subprocess


LOGS_DIR = "./logs"
LOG_FILE = os.path.join(LOGS_DIR, "backup_manager.log")
SERVICE_SCRIPT = "backup_service.py"


def log(message):
    os.makedirs(LOGS_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("[%d/%m/%Y %H:%M]")
    entry = f"{timestamp} {message}\n"
    with open(LOG_FILE, "a") as f:
        f.write(entry)

SCHEDULES_FILE = "backup_schedules.txt"

def is_valid_schedule(schedule):
    parts = schedule.strip().split(";")
    if len(parts) != 3:
        return False
    path, time_str, name = parts
    if not path or not time_str or not name:
        return False

    time_parts = time_str.split(":")
    if len(time_parts) != 2:
        return False
    hh, mm = time_parts
    if not hh.isdigit() or not mm.isdigit():
        return False
    if not (0 <= int(hh) <= 23 and 0 <= int(mm) <= 59):
        return False

    return True

def cmd_create(schedule):
    if not is_valid_schedule(schedule):
        log(f"Error: malformed schedule: {schedule}")
        print(f"Error: malformed schedule: {schedule}")
        return

    with open(SCHEDULES_FILE, "a") as f:
        f.write(schedule.strip() + "\n")

    log(f"New schedule added: {schedule.strip()}")
    print(f"Schedule added: {schedule.strip()}")


def read_schedules():
    with open(SCHEDULES_FILE, "r") as f:
        lines = f.readlines()
    return [line.strip() for line in lines if line.strip()]
    

def cmd_list():
    # print("list")
    try:
        schedules = read_schedules()
        log("Show schedules list")
        if not schedules:
            print("No schedule found.")
            return
        for i, schedule in enumerate(schedules):
            print(f"{i}: {schedule}")

    except FileNotFoundError:
        log("Show schedules list: no schedules found")
        print("No schedule found.")

def write_schedules(schedules):
    with open(SCHEDULES_FILE, "w") as f:
        for schedule in schedules:
            f.write(schedule + "\n")

def cmd_delete(index_str):
    try:
        index = int(index_str)
    except ValueError:
        log(f"Error: invalid index: {index_str}")
        print(f"Error: invalid index: {index_str}")
        return

    try:
        schedules = read_schedules()
        if index < 0 or index >= len(schedules):
            log(f"Error: can't find schedule at index {index}")
            print(f"Error: can't find schedule at index {index}")
            return
        schedules.pop(index)
        write_schedules(schedules)
        log(f"Schedule at index {index} deleted")
        print(f"Schedule at index {index} deleted.")
    except FileNotFoundError:
        log("Error: can't find backup_schedules.txt")
        print("Error: can't find backup_schedules.txt")

def cmd_start():
    pid_file = os.path.join(LOGS_DIR, "backup_service.pid")

    # Check if already running
    if os.path.exists(pid_file):
        with open(pid_file, "r") as f:
            old_pid = f.read().strip()
        if old_pid and os.path.exists(f"/proc/{old_pid}"):
            log("Error: backup_service already running")
            print("Error: backup_service already running")
            return

    try:
        proc = subprocess.Popen(
            [sys.executable, SERVICE_SCRIPT],
            start_new_session=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        os.makedirs(LOGS_DIR, exist_ok=True)
        with open(pid_file, "w") as f:
            f.write(str(proc.pid))
        log("backup_service started")
        print(f"backup_service started (PID {proc.pid})")
    except Exception as e:
        log(f"Error: could not start backup_service: {e}")
        print(f"Error: could not start backup_service: {e}")

def cmd_stop():
    pid_file = os.path.join(LOGS_DIR, "backup_service.pid")

    try:
        with open(pid_file, "r") as f:
            pid = int(f.read().strip())
        os.kill(pid, 9)
        os.remove(pid_file)
        log("backup_service stopped")
        print("backup_service stopped.")
    except FileNotFoundError:
        log("Error: can't stop backup_service")
        print("Error: can't stop backup_service (no PID file found)")
    except ProcessLookupError:
        os.remove(pid_file)
        log("Error: can't stop backup_service")
        print("Error: backup_service was not running.")
    except Exception as e:
        log(f"Error: can't stop backup_service: {e}")
        print(f"Error: can't stop backup_service: {e}")

def cmd_backups():
    print("backups")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 backup_manager.py <command>")
        return

    command = sys.argv[1]

    if command == "create":
        if len(sys.argv) < 3:
            print("Error: provide a schedule. Format: \"path;HH:MM;name\"")
        else:
            cmd_create(sys.argv[2])

    elif command == "list":
        cmd_list()

    elif command == "delete":
        if len(sys.argv) < 3:
            print("Error: provide an index number to delete.")
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
        print(f"Error: unknown command '{command}'")

if __name__ == "__main__":
    main()