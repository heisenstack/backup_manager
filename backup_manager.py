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

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 backup_manager.py <command>")
        return

    command = sys.argv[1]
    print(f"{command}")

if __name__ == "__main__":
    main()