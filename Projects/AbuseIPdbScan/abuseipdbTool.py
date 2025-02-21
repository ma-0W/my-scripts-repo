#!/usr/bin/env python3
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
os.system("title AbuseIPdb Scan")
os.system('mode con: cols=55 lines=26')
os.system("color 02")

# Get abuseipdb API key from windows environment variables (YOU NEED TO STORE THE API KEY IN YOUR ENVIRONMENT VARIABLES WITH THE SAME NAME), return an error if not found. 
def get_api_key():
    api_key = os.environ.get("abuse_ip_db")
    if not api_key:
        raise ValueError("API Key 'abuse_ip_db' not found. Make sure it's set in your environment variables.")
    return api_key

api_key = get_api_key()
"""
Send a GET request to abuseIPDB API to check if the inputted IP has been reported in the last 
90 days for abusive behavior.
"""
def check_abuseipdb(ipAddress):
    api_base = 'https://api.abuseipdb.com/api/v2/check'
    # Query Parameters
    querystring = {
        'ipAddress': ipAddress,
        # Optionally include how far back you want to check. default 30, min 1, max 365
        'maxAgeInDays': '90'
    }
    # Tell the server to send the response in JSON format
    # Provide API Key for authenticaiton
    headers = {
        'Accept': 'application/json',
        'Key': api_key
    }
    # HTTP Request - requests.get() call sends the request with the URL, headers and parameters.
    response = requests.get(api_base, headers=headers, params=querystring)
    # Convert the text from API to JSON. 
    # Error handling
    
    try:
        # Check for HTTP errors
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        # Return error code
        return {"error": f"HTTP error occurred: {http_err}"}

    # Check for malformed Json
    try:
        return response.json()
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response"}

# check if clipboard content is an IP. Further prevents spamming the API with random content.
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
                result = check_abuseipdb(current_clipboard)
                # Pretty print the JSON response.
                print(json.dumps(result, sort_keys=True, indent=4))
                print("-" * 55)  # Separator for readability
            else:
                print("Not a valid IP")
        time.sleep(2)

if __name__ == '__main__':
    main()
