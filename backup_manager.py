import os
import sys
from datetime import datetime

LOGS_DIR = "./logs"
LOG_FILE = os.path.join(LOGS_DIR, "backup_manager.log")

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

def cmd_list():
    print("list")

def cmd_delete(index):
    print(f"delete {index}")

def cmd_start():
    print("start")

def cmd_stop():
    print("stop")

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