# pip install win10toast
import os
import datetime
import logging
from win10toast import ToastNotifier # for desktop notifications

# Get the directory where the script resides
script_dir = os.path.dirname(os.path.realpath(__file__))

# Configure logging.
# This sets up logging so that messages with level INFO or higher are written to 'monitor.log'
logging.basicConfig(
    filename= os.path.join(script_dir, 'alerts.log'),    # Log file name
    # All log messages at the INFO level and higher (Warning etc) will be recorded.
    level=logging.INFO, # Log level (INFO, WARNING, ERROR, etc.). 
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

toaster = ToastNotifier()

def import_logs():
    file_path = os.path.join(script_dir, "simulated_security.log")
    with open(file_path, "r") as f:
        return f.readlines()

# Parse through the logs, if log contains the keyword "CRITICAL", append it to the list and return the list.
def parse_logs():
    critical_Logs = []
    logs = import_logs()
    for log in logs:
        if "CRITICAL" in log or "WARNING" in log:
            critical_Logs.append(log)
    return critical_Logs

def upload_logs():
    # get and assign the list of critical/warning logs using the parse_logs()
    logs = parse_logs()
    output_file = os.path.join(script_dir, "Investigate.log")
    # "w" overwrites the investigate.log file each time the script is ran
    with open(output_file, "w") as parsedOutputs:
        # iterate through the list of logs and write each element of the list to the parsed Outputs file. 
        for log in logs:
            parsedOutputs.write(log)
            print(log)

    # If we have any critical or warning logs, send a notification
    if logs:
        notification_message = f"{len(logs)} critical/warning log(s) found. Check {output_file}"
        toaster.show_toast("Security Alert", notification_message, duration=10)
        logging.info("Notification sent: " + notification_message)
    else:
        logging.info("No critical or warning logs found.")
    
upload_logs()