import os
from datetime import datetime, timedelta
import time 
import tempfile
import shutil
from pathlib import Path

def create_zip(base_folder: Path, *, filter_by_date=False, days_ahead=14) -> Path | None:
    """
    Create a zip of the given base_folder.
    - If filter_by_date=True: include only folders with ddmmyy names between today and today+days_ahead.
    - Otherwise: include all files directly inside the folder.
    Returns the path to the zip file, or None if the folder doesn't exist.
    """
    if not base_folder.exists():
        return None

    temp_dir = tempfile.TemporaryDirectory()
    temp_path = Path(temp_dir.name)

    if filter_by_date:
        # For 'sessions' type folders (named ddmmyy)
        today = datetime.now().date()
        end_date = today + timedelta(days=days_ahead)

        for folder in base_folder.iterdir():
            if folder.is_dir():
                try:
                    session_date = datetime.strptime(folder.name, "%d%m%y").date()
                    if today <= session_date <= end_date:
                        shutil.copytree(folder, temp_path / folder.name)
                except ValueError:
                    continue  # Ignore folders not matching ddmmyy format
    else:
        # For flat directories containing only files
        for item in base_folder.iterdir():
            if item.is_file():
                shutil.copy2(item, temp_path / item.name)

    # Create a zip archive of the collected contents
    zip_name = "sessions_selected" if filter_by_date else "requests_files"
    zip_path = temp_path / zip_name
    zip_file = shutil.make_archive(str(zip_path), 'zip', temp_path)
    return Path(zip_file)

def addToWaitlist(session,username:str):
    students = session.SRGet("session","students")
    waitlist = session.SRGet("session","waitlist")
    places = int(session.SRGet("session","places")[0])
    if username in students:
        print(f"{username} is already enrolled in the session.")
        return
    if username in waitlist:
        print(f"{username} is already in the waitlist.")
        return
    if len(students) < places:
        session.SRChange("session","students",username,add=True)
        print(f"{username} added to session students.")
    else:
        session.SRChange("session","waitlist",username,add=True)
        print(f"{username} added to waitlist.")