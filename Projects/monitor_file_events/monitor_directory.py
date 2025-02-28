import time
import os
import logging
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

# Get the directory where the script resides
script_dir = os.path.dirname(os.path.realpath(__file__))

# Configure logging.
# This sets up logging so that messages with level INFO or higher are written to 'monitor.log'
logging.basicConfig(
    filename= os.path.join(script_dir, 'monitor.log'),    # Log file name
    # All log messages at the INFO level and higher (Warning etc) will be recorded.
    level=logging.INFO, # Log level (INFO, WARNING, ERROR, etc.). 
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

target_dir = r"C:\Users\Haaris\Pictures"

# FileSystemEventHandler is a class that you can subclass to define custom actions when events occur
class MyEventHandler(FileSystemEventHandler):
    """  
    on_any_event is called by the observer whenever a filesystem event occurs 
    in the monitored directory. It takes an event parameter 'FileSystemEvent' and prints it. 
    """
    
    def on_any_event(self, event: FileSystemEvent) -> None: # FileSystemEvent is a base class for events like (file creation, modification, deletion etc.)
        # log file event info
        logging.info(event)
        print(event)

# MyEventHandler is a subclass of FileSystemEventHandler.  
event_handler = MyEventHandler()
# instance of the observer class which monitors a directory and dispatches events to handler
observer = Observer()
# specifies to the observer to use the custom event handler for all events
# "." = current working directory (and its subdirectories)
# recursive = true means that the observe will monitor all subdirectories of the current directory also.
observer.schedule(event_handler, target_dir, recursive=True)
# start the observe in a seperate thread to watch for filesystem events
observer.start()

# infinite loop
try:
    while True:
        time.sleep(1)
# When the loop is interrupted (program is exited), the finally block executes.
# stops the observer from monitoring and waits for the thread to terminate cleanly. 
finally:
    observer.stop()
    observer.join()