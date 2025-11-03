import os
from datetime import datetime, timedelta
import time 
import tempfile
import shutil
from pathlib import Path

def create_sessions_zip(base_folder: Path, days_ahead: int = 14) -> Path | None:
    if not base_folder.exists():
        return None

    today = datetime.now().date()
    end_date = today + timedelta(days=days_ahead)

    temp_dir = tempfile.TemporaryDirectory()
    temp_path = Path(temp_dir.name)

    for folder in base_folder.iterdir():
        if folder.is_dir():
            try:
                session_date = datetime.strptime(folder.name, "%d%m%y").date()
                if today <= session_date <= end_date:
                    shutil.copytree(folder, temp_path / folder.name)
            except ValueError:
                continue 

    zip_path = temp_path / "sessions_selected"
    zip_file = shutil.make_archive(str(zip_path), 'zip', temp_path)
    return Path(zip_file)
    