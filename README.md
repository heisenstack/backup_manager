# Backup Manager

A simple automated backup system built with Python. It runs in the background, checks a schedule, and compresses directories into `.tar` files automatically.

## How it works

Two scripts work together:

- `backup_manager.py` — the one you interact with from the terminal
- `backup_service.py` — runs silently in the background and does the actual backups

## Setup

No external libraries needed, just Python 3.

Clone or copy the project folder, then you're good to go.

## Usage

### Add a backup schedule
```bash
python3 backup_manager.py create "path/to/folder;HH:MM;backup_name"
```
Example:
```bash
python3 backup_manager.py create "documents;14:30;my_docs"
```

### List scheduled backups
```bash
python3 backup_manager.py list
```

### Delete a schedule
```bash
python3 backup_manager.py delete 0
```

### Start the backup service
```bash
python3 backup_manager.py start
```

### Stop the backup service
```bash
python3 backup_manager.py stop
```

### List completed backups
```bash
python3 backup_manager.py backups
```

## Project structure
backup-manager/
├── backup_manager.py       # CLI — manage schedules and control the service
├── backup_service.py       # Background worker — runs backups on schedule
├── backup_schedules.txt    # Created automatically when you add a schedule
├── logs/
│   ├── backup_manager.log  # Logs every command you run
│   └── backup_service.log  # Logs every backup the service performs
└── backups/                # Your .tar backup files end up here

## Notes
- Schedules that have already run are automatically removed
- The service checks schedules every 45 seconds
- All errors are logged, the scripts won't crash on bad input
