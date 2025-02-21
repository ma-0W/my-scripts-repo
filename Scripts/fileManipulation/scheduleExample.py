import schedule
import time

def job():
    print("This job runs every 5 seconds.")

schedule.every(5).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)

""" 
You might write scripts that automatically archive log files, search for errors 
in logs, or rotate logs when they reach a certain size.
"""