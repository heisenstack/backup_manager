import os
import time
import tarfile
from datetime import datetime

SCHEDULES_FILE = "backup_schedules.txt"
LOGS_DIR       = "./logs"
BACKUPS_DIR    = "./backups"
LOG_FILE       = os.path.join(LOGS_DIR, "backup_service.log")
SLEEP_SECONDS  = 45

def log(message):
    os.makedirs(LOGS_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("[%d/%m/%Y %H:%M]")
    entry = f"{timestamp} {message}\n"
    with open(LOG_FILE, "a") as f:
        f.write(entry)

def read_schedules():
    with open(SCHEDULES_FILE, "r") as f:
        return [line.strip() for line in f if line.strip()]

def write_schedules(schedules):
    with open(SCHEDULES_FILE, "w") as f:
        for s in schedules:
            f.write(s + "\n")

def check_and_run_schedules():
    try:
        schedules = read_schedules()
    except FileNotFoundError:
        return

    now           = datetime.now()
    current_total = now.hour * 60 + now.minute

    remaining  = []
    to_process = []

    for schedule in schedules:
        parts = schedule.split(";")
        if len(parts) != 3:
            continue
        path, time_str, name = parts
        hh, mm = time_str.split(":")
        sched_total = int(hh) * 60 + int(mm)

        if current_total >= sched_total:
            to_process.append((path, name))
        else:
            remaining.append(schedule)

    for path, name in to_process:
        perform_backup(path, name)

    write_schedules(remaining)


def perform_backup(path, name):
    os.makedirs(BACKUPS_DIR, exist_ok=True)
    tar_path = os.path.join(BACKUPS_DIR, f"{name}.tar")

    try:
        with tarfile.open(tar_path, "w") as tar:
            tar.add(path, arcname=os.path.basename(path))
        log(f"Backup done for {path} in {tar_path}")
    except FileNotFoundError:
        log(f"Error: source path not found: {path}")
    except PermissionError:
        log(f"Error: permission denied for path: {path}")
    except Exception as e:
        log(f"Error: backup failed for {path}: {e}")

        
def main():
    log("backup_service started")
    while True:
        try:
            check_and_run_schedules()
        except Exception as e:
            log(f"Error: unexpected error: {e}")
        time.sleep(SLEEP_SECONDS)

if __name__ == "__main__":
    main()