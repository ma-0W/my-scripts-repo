import os
import shutil

def copy_all_files(source_dir, destination_dir):
    """
    Copies all files from source_dir to destination_dir.
    This function does not copy subdirectories, only files in the root of the source_dir
    """
    # Ensure the destination directory exists; create it if it doesn't
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
        print(f"Created destination directory {destination_dir}")

    # list files in the source directory
    files = os.listdir(source_dir)

    # loop over each item
    for file_name in files:
        # build the full file paths for the source and destination
        # joins the files names to the rest of their paths
        source_file = os.path.join(source_dir, file_name)
        destination_file = os.path.join(destination_dir, file_name) 

        # check if the current item is a file (skip directories).
        if os.path.isfile(source_file):
            try:# shutil.copy2 is used to copy files along with their metadata
                shutil.copy2(source_file, destination_file)
                print(f"Copied {source_file} to {destination_file}")
            except Exception as e:
                print(f"Error copying {source_file}: {e}")

source_directory = r"C:\Users\Haaris\Pictures"
destination_directory = r"C:\Users\Haaris\Pictures\destination"
copy_all_files(source_directory, destination_directory)