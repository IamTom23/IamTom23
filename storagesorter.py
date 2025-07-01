import os
import shutil
import schedule
import time

# Source folder
source_directory = os.path.expanduser(r"C:\Users\ThomasRutt\Downloads")

# Destination base folder
destination_base = os.path.expanduser(r"C:\Users\ThomasRutt\Downloads")

# File type categories
file_types = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "Documents": [".pdf", ".csv", ".docx", ".doc", ".txt", ".xlsx", ".pptx"],
    "Videos": [".mp4", ".avi", ".mov", ".mkv"],
    "Audio": [".mp3", ".wav", ".aac"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
}

def organise_files():
    print("🔄 Organizing files...")
    for filename in os.listdir(source_directory):
        file_path = os.path.join(source_directory, filename)

        if os.path.isfile(file_path):
            moved = False
            _, ext = os.path.splitext(filename)

            for folder, extensions in file_types.items():
                if ext.lower() in extensions:
                    target_folder = os.path.join(destination_base, folder)
                    os.makedirs(target_folder, exist_ok=True)
                    shutil.move(file_path, os.path.join(target_folder, filename))
                    print(f"✅ Moved {filename} to {folder}/ in Downloads")
                    moved = True
                    break

            if not moved:
                other_folder = os.path.join(destination_base, "others")
                os.makedirs(other_folder, exist_ok=True)
                shutil.move(file_path, os.path.join(other_folder, filename))
                print(f"📁 Moved {filename} to others/ in Downloads")




organise_files()

