import os
from datetime import datetime, timedelta
import time 
import tempfile
import shutil
from pathlib import Path
import io
import zipfile
from session import Session

def create_zip(base_folder: Path, *, filter_by_date=False, days_ahead=14) -> Path | None:
    """
    Create a zip of the given base_folder.
    - If filter_by_date=True: include only folders with ddmmyy names between today and today+days_ahead.
    - Otherwise: include all files directly inside the folder.
    Returns the path to the zip file, or None if the folder doesn't exist.
    """
    if not base_folder.exists():
        return None

    # We'll create a temporary working directory for collecting files, then
    # write the final zip into the repository working directory so it remains
    # available to send_file after this function returns.
    temp_dir = tempfile.mkdtemp()
    temp_path = Path(temp_dir)

    try:
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

        # Create a zip archive of the collected contents in the repo cwd so it
        # remains after this function returns.
        zip_base = Path.cwd() / ("sessions_selected" if filter_by_date else "requests_files")
        zip_file = shutil.make_archive(str(zip_base), 'zip', temp_path)
        return Path(zip_file)
    finally:
        # Clean up the temporary directory used for collection
        try:
            shutil.rmtree(temp_path)
        except Exception:
            pass

def create_zip_bytes(base_folder: Path, *, filter_by_date=False, days_ahead=14) -> io.BytesIO | None:
    """
    Create a ZIP archive in-memory and return a BytesIO containing the zip.
    Returns None if base_folder doesn't exist or has no content to include.
    """
    if not base_folder.exists():
        return None

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        if filter_by_date:
            today = datetime.now().date()
            end_date = today + timedelta(days=days_ahead)
            for folder in base_folder.iterdir():
                if folder.is_dir():
                    try:
                        session_date = datetime.strptime(folder.name, "%d%m%y").date()
                        if today <= session_date <= end_date:
                            # add folder and files inside it
                            for root, _, files in os.walk(folder):
                                rel_root = Path(root).relative_to(base_folder)
                                for f in files:
                                    full = Path(root) / f
                                    arcname = str(rel_root / f)
                                    zf.write(full, arcname=arcname)
                    except ValueError:
                        continue
        else:
            for item in base_folder.iterdir():
                if item.is_file():
                    zf.write(item, arcname=item.name)

    buf.seek(0)
    return buf

def addToWaitlist(session,username:str):
    students = session.SRGet("session","students")
    waitlist = session.SRGet("session","waitlist")
    places = int(session.SRGet("session","places")[0])
    if username in students:
        print(f"{username} is already enrolled in the session.")
        raise Exception(f"error1")
    if username in waitlist:
        print(f"{username} is already in the waitlist.")
        raise Exception(f"error2")
    if len(students) < places:
        session.SRChange("session","students",username,add=True)
        print(f"{username} added to session students.")
    else:
        session.SRChange("session","waitlist",username,add=True)
        print(f"{username} added to waitlist.")

def sessionCleanup():
    current_date = datetime.now().date()
    sessionsPath = Path("sessions")

    for sessionDate in sessionsPath.iterdir():
        try:
            sessionDate2 = datetime.strptime(sessionDate.name, "%d%m%y").date()
        except ValueError:
            raise ValueError(f"Folder name {sessionDate.name} is not in ddmmyy format")
        if sessionDate2 < current_date:
            try:
                shutil.rmtree(sessionDate)
                print(f"Deleted session folder: {sessionDate}")
            except Exception as e:
                print(f"Error deleting session folder {sessionDate}: {e}")


if __name__ == '__main__':
    print("Starting server internal update loop")
    loopid = 0 
    while True:
        print("updating sessions...")
        if loopid >= 1440:
            print("Resetting loop counter")
            loopid = 0
        if loopid % 60 == 0:
            print("Session cleanup check...")
            sessionCleanup()
        
        loopid += 1
        time.sleep(60)