import requests
import os
import json
import pyperclip
import time
import ctypes
import win32gui
import win32con
import ipaddress

# Set the console window to always be ontop
hwnd = ctypes.windll.kernel32.GetConsoleWindow()
win32gui.SetWindowPos(hwnd,win32con.HWND_TOPMOST,0,0,0,0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW)

# Resize and give it a hacker vibe
os.system("title VirusTotalScan")
os.system('mode con: cols=40 lines=15')
os.system("color 02")

# Get VirusTotal API key from windows environment variables (YOU NEED TO STORE THE API KEY IN YOUR ENVIRONMENT VARIABLES WITH THE SAME NAME), return an error if not found. 
def get_api_key():
    api_key = os.environ.get("virustotal_api_key")
    if not api_key:
        raise ValueError("API Key 'virustotal_api_key' not found. Make sure it's set in your environment variables.")
    return api_key

api_key = get_api_key()

# Send a get request to VirusTotal including your api key in the header.
def check_ip(ip):
    url = "https://www.virustotal.com/api/v3/ip_addresses/{0}".format(ip)
    headers = {
        "accept": "application/json",
        "x-apikey": api_key
    }

    # HTTP Request - requests.get() call sends the request with the URL, headers and parameters.
    response = requests.get(url, headers=headers)
    # Convert the text from API to JSON. 
    # Error handling
    
    try:
        # Check for HTTP errors
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        # return error code
        return {"error": f"HTTP error occurred: {http_err}"}

    try:
        return response.json()
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response"}

# Check if clipboard content is an IP. Further prevents spamming the API with random content.
def is_valid_ip(ip_string):
    try:
        ipaddress.ip_address(ip_string)
        return True
    except ValueError:
        return False

# Main loop
def main():
    previous_clipboard = ""
    # Run loop indefinitely
    while True:
        current_clipboard = pyperclip.paste().strip()
        # Avoid spamming the API by only acting when the clipboard content changes.
        if current_clipboard != previous_clipboard:
            previous_clipboard = current_clipboard
            if is_valid_ip(current_clipboard):
                print("Searching for: " + current_clipboard)
                result = check_ip(current_clipboard)
                filtered_result = {
                    "IP": result.get("data", {}).get("id"),
                    "Last Analysis Stats": result.get("data", {}).get("attributes", {}).get("last_analysis_stats"),
                }
                # Pretty print the JSON response.
                print(json.dumps(filtered_result, sort_keys=True, indent=4))
                print("-" * 40)  # Separator for readability
                
        time.sleep(2)

if __name__ == '__main__':
    main()

