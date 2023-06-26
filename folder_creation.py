# Run before any other file
import os
from config import cur_path


def create_folder_structure():
    base_folder = os.path.join(cur_path, "Data")
    subfolders = {
        "Green Taxi": ["Individual CSVs", "Parquet Files"],
        "Yellow Taxi": ["Individual CSVs", "Parquet Files"]
    }

    try:
        # Create the base folder
        os.mkdir(base_folder)
        
        # Create subfolders inside the base folder
        for subfolder in subfolders:
            subfolder_path = os.path.join(base_folder, subfolder)
            os.mkdir(subfolder_path)
            
            # Create sub-subfolders inside the subfolders
            for sub_subfolder in subfolders[subfolder]:
                sub_subfolder_path = os.path.join(subfolder_path, sub_subfolder)
                os.mkdir(sub_subfolder_path)
        
        print("Folder structure created successfully!")
    except OSError as e:
        print(f"Error: {e.strerror}")

# Call the function to create the folder structure
create_folder_structure()
