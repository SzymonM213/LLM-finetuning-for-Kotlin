import os
import shutil

def move_files_to_data_directory(project_dir, data_dir, proper_extensions):
    for root, _, files in os.walk(project_dir):
        for file in files:
            _, extension = os.path.splitext(file)
            if extension.lower() in proper_extensions:
                os.makedirs(data_dir, exist_ok=True)
                
                src_path = os.path.join(root, file)
                dest_path = os.path.join(data_dir, file)
                shutil.copy(src_path, dest_path)

if __name__ == "__main__":
    project_directory = "kotlin"
    data_directory = "data/kotlin"
    kotlin_extensions = [".kt", ".kts"]
    move_files_to_data_directory(project_directory, data_directory, kotlin_extensions)