""" 
Create a Script that Deletes Files Older than 30 Days
Write a Python script that scans a directory,
checks each file's modification time, and deletes any files older than 30 days.
"""
import os
import datetime
import logging

# Get the directory where the script resides
script_dir = os.path.dirname(os.path.realpath(__file__))

# Configure logging.
# This sets up logging so that messages with level INFO or higher are written to 'fileDeletion.log'
logging.basicConfig(
    filename= os.path.join(script_dir, 'fileDeletion.log'),    # Log file name
    # All log messages at the INFO level and higher (Warning etc) will be recorded.
    level=logging.INFO, # Log level (INFO, WARNING, ERROR, etc.). 
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


"""
Scans the specified directory and deletes files that have not been modified
in the last x days. Logs the actions taken.
"""
def find_old_files(src_dir, days_threshold=30):
    today = datetime.datetime.today()
    
    
    try:
        files = os.listdir(src_dir)
    except Exception as e:
        logging.error(f"Error listing files in directory {src_dir}: {e}")
        return
    
    for file_name in files:
        # create the full path for the current file in the list
        source_file = os.path.join(src_dir, file_name)
        
        # Ensure that we are deleting a file and not a directory
        if os.path.isfile(source_file):
            file_timestamp = os.path.getmtime(source_file)
            # convert the timestamp to a datetime object
            timeobj = datetime.datetime.fromtimestamp(file_timestamp)
           
            # when you subtract one datetime from another, python returns a timedelta object.
            # the object represents the amount of time between the two dates.
            # so, THIS IS NOT A SIMPLE SUBTRACTION
            time_delta = today - timeobj

            # log the age of the file
            logging.info(f"{source_file} - Age: {time_delta.days} days")
            print(f"{source_file} - Age: {time_delta.days} days")

            # check if its older than threshold, delete the file
            if time_delta.days > days_threshold:
                print(f"{source_file} is an old file and shall be deleted.")
                try:
                    os.remove(source_file)
                    logging.info(f"Deleted file: {source_file}")
                except Exception as e:
                    print(f"Error deleting {source_file}: {e}")
                    logging.error(f"Error deleting {source_file}: {e}")
            else:
                print(f"{source_file} is still within the threshold.")
        else:
            print(f"{source_file} is not a file. Skipping.")


source_directory = r"C:\Users\Haaris\Pictures\agetest" 

find_old_files(source_directory, 5)