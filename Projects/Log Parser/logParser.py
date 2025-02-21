# Log parser
import os

# Read the sample log file: Load the file line by line in the script.
# Filter for specific keywords: Search for key phrases that indicate issues.
# Write the matching logs to a new file: Save the filtered entries for later review.

def import_logs():
    # Create an empty list object
    lines = []
    #open file and read line by line
    script_path = os.path.realpath(__file__) # Gets the current path for the script that we are runnnig
    # gets folder name for the running script
    # splits the result into something like this "("/home/user/myproject", "myscript.py")"
    script_folder = os.path.split(script_path)[0] # 0 added to the end to remove the myscript.py from the tuple, this allows us to just take the directory.
    file_path = os.path.join(script_folder, "exampleLog.txt")
    # adjusted to use a context manager. It return a list of lines and ensure the file is closed immediately.
    with open(file_path, "r") as f:
        return f.readlines()

# Parse through the logs, if log contains the keyword "CRITICAL", append it to the list and return the list.
def parse_logs():
    critical_Logs = []
    logs = import_logs()
    for log in logs:
        if "CRITICAL" in log:
            critical_Logs.append(log)
    return critical_Logs


def upload_logs():
    # get and assign the list of critical logs using the parse_logs()
    logs = parse_logs()
    with open("parsedOutputs.txt", "w") as parsedOutputs:
        # iterate through the list of logs and write each element of the list to the parsed Outputs file. 
        for log in logs:
            parsedOutputs.write(log)
    
upload_logs()