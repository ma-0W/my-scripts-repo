import requests
import os
import json
import logging
import schedule
import time
from datetime import datetime

# Get the directory where the script resides
script_dir = os.path.dirname(os.path.realpath(__file__))

# Create the full path to the log file in the script's directory and declare the file name
error_log_file = os.path.join(script_dir, "weatherError.log")
output_log_file = os.path.join(script_dir, "weatherOutput.log")

# The error log file will be written in the same folder where the script is located
logging.basicConfig(
    filename= error_log_file, 
    format = '%(asctime)s %(message)s',             
    encoding='utf-8', 
    level = logging.WARNING
)

# Get WeatherStack API key from windows environment variables. 
def get_api_key():
    api_key = os.environ.get("weather_stack")
    if not api_key:
        raise ValueError("API Key 'weather_stack' not found. Make sure it's set in your environment variables.")
    return api_key

api_key = get_api_key()
url = "https://api.weatherstack.com/current?access_key={0}".format(api_key)
querystring = {"query":"London"}

def get_weather_london():
    try: 
        response = requests.get(url, params=querystring)
        response.raise_for_status()
        result = response.json()
        # print(response.status_code) to view status code 
    
        # Check if the result contains an error key.
        if 'error' in result:
            error_message = json.dumps(result['error'], sort_keys=True, indent=4)
            print("Error from API:")
            print(error_message)
            logging.warning(error_message)
        else:
            filtered_result = {
                "Location": result.get("request", {}).get("query"),
                "Local Time": result.get("location", {}).get("localtime"),
                "Time of observation": result.get("current", {}).get("observation_time"),
                "Daytime?": result.get("current", {}).get("is_day"),
                "Feels like": result.get("current", {}).get("feelslike"),
                "Temperature": result.get("current", {}).get("temperature"),
                "Uv index": result.get("current", {}).get("uv_index"),
                "Weather Description": result.get("current", {}).get("weather_descriptions")
            }
            
            output_message = json.dumps(filtered_result, sort_keys=False, indent=4) # Sort keys true would sort it alphabetically
            print(output_message)
            # Write the API output to the weatherOutput.log
            with open(output_log_file, "a", encoding="utf-8") as outf:
                outf.write(output_message + "\n")

    except requests.exceptions.HTTPError as http_err:
        print(f"Http error occured(Bad status code): {http_err}")
        logging.warning(http_err)

    except Exception as err:
        print(f"Other error occured: {err}")
        logging.warning(err)

schedule.every().hour.do(get_weather_london)

while True: 
    schedule.run_pending()
    time.sleep(1)