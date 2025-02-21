"""
Common routine taks to automate:
File management
- renaming files in bulk
- moving or copying files from directories
- deleting or archiving old files

System Tasks:
- schedulling scripts to run at certain times
- checking system health logs
- cleaning temporary directories

LETS RENAME ALL YOUR IMAGE FILES WAHOOOOOOO!
"""

 
import os
# define the directory that contains the files for renaming
directory = r"C:\Users\Haaris\Pictures\agetest"

# loop over files in the directory, rename them and handle errors if they occur 
def rename_files(directory):
    # get a list of files in the directory
    files = os.listdir(directory)
    # filter out files which are not images
    image_files = [f for f in files if f.lower().endswith((".jpg", ".jpeg", ".png"))]

    # rename each file with a new name format 
    for idx, filename in enumerate(sorted(image_files), start=1):
        # construct the new file name using zero padding for consistency {idx:03d} ensures that numbers are padded with zeros (e.g., 001, 002).
        new_name = f"image_{idx:03d}.jpg"
        old_path = os.path.join(directory, filename)
        new_path = os.path.join(directory, new_name)
        # while looping over the sorted list rename each using os.rename()
        try:
            os.rename(old_path, new_path)
            print(f"Renamed {filename} to {new_name}")
        except Exception as e:
            print(f"Error renaming {filename}: {e}")

rename_files(directory)
 

