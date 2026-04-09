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

def create(schedule):
    print(f"create {schedule}")

def list():
    print("list")

def delete(index):
    print(f"delete {index}")

def start():
    print("start")

def stop():
    print("stop")

def backups():
    print("backups")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 backup_manager.py <command>")
        return

    command = sys.argv[1]

    if command == "create":
            create(sys.argv[2])

    elif command == "list":
        list()

    elif command == "delete":
            delete(sys.argv[2])

    elif command == "start":
        start()

    elif command == "stop":
        stop()

    elif command == "backups":
        backups()

    else:
        log(f"Error: unknown command: {command}")
        print(f"Error: unknown command '{command}'")

if __name__ == "__main__":
    main()