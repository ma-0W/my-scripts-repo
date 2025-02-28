#!/usr/bin/env python3
# Script that scans files using VirusTotal API v3
# https://developers.virustotal.com/reference
# for http requests
import requests
# hashing file contents
import hashlib
# for sleep between api requests
import time
# accessing environment variables and file system paths
import os

# Retrieve API key from environment variables (needs to be changed for linux)
def get_api_key():
    api_key = os.environ.get("virustotal_api_key")
    if not api_key:
        raise ValueError("API Key 'virustotal_api_key' not found. Make sure it's set in your environment variables.")
    return api_key



def check_virustotal_hash(token, file_hash):
    
    # Check if the file hash exists in VirusTotal's database.
    url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
    # include API key in the header of the request
    headers = {"x-apikey": token}

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()  # Return JSON response if successful
    elif response.status_code == 404:
        return None  # File not found
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def upload_virustotal_file(token, file_path): 
    
    # Upload a file to VirusTotal for scanning.
    url = "https://www.virustotal.com/api/v3/files"
    headers = {"x-apikey": token}

    # Open the file in binary mode
    with open(file_path, "rb") as file:
        files = {"file": (file_path, file)}
        response = requests.post(url, headers=headers, files=files)

    if response.status_code in [200, 201]:
        print("File uploaded successfully!")
        return response.json()
    else:
        print(f"File upload failed: {response.status_code}, {response.text}")
        return None

def hash_file(file_path):
    
    # Generate SHA-256 hash for the file.
    buffer_size = 65536  # The file is read in chunks, each chunk is a bytes object
    sha256 = hashlib.sha256()

    with open(file_path, 'rb') as f:
        while chunk := f.read(buffer_size):
            sha256.update(chunk)

    return sha256.hexdigest()

# Get API key from environment variables
token = get_api_key()
api_base = "https://www.virustotal.com/api/v3"

# User prompted for filepath input for scanning  
target_file = input("What file do you wish to scan? ").strip()
# format the path for windows
target_file = os.path.normpath(target_file)

# Confirm the file exists
if not os.path.isfile(target_file):
    print("Error: File not found!")
    exit(1)

# Generate SHA-256 hash of the file
file_hash = hash_file(target_file)

# Check if the file has been scanned before
# file check is then assigned a dictionary containing scan results if the file was found, or
# is none if the file was not previously scanned
file_check = check_virustotal_hash(token, file_hash)

if file_check:
    # Extract scan results
    """
    The following is a representation of how the returned json data from the API the JSON data 
    is automatically converted into a dictionary. 

     file_check = {
    "data": {
        "attributes": {
            "last_analysis_stats": {
                "harmless": 70,
                "malicious": 5,
                "suspicious": 3,
                "undetected": 22
            }
        }
    }
}

    The dictionary is nested, the top level dictionary has a key called 'data', the value of data
    is another dictionary 'attributes'. 
    
    The value of attributes is another key(dictionary) which is 'last_analysis_stats"  which
    has the results of the scan. 
   
    """
    # .get() is used to safely access the nested values
    scan_results = file_check.get("data", {}).get("attributes", {})
    # if scan results is not none(empty), meaning that the dictionaries had values.
    if scan_results:
        print(f"Scan found: {scan_results.get('last_analysis_stats')}")
        print(f"More details: https://www.virustotal.com/gui/file/{file_hash}")
        exit(0)  # Exit early if scan results exist
    else:
        print("ℹ️ Scan found, but no details available.")
else:
    print("File not previously scanned, submitting...")

    upload_response = upload_virustotal_file(token, target_file)
    
    if upload_response:
        print("File uploaded, waiting for results (max 2 min)...")

        # Max of 6 loops, with a pause
        for i in range(6):
            time.sleep(21)  # Wait 21 seconds before checking again

            # Check for scan results
            file_check = check_virustotal_hash(token, file_hash)
            if file_check:
                print("Results returned:")
                print(f"Scans tested: {file_check.get('data', {}).get('attributes', {}).get('last_analysis_stats')}")
                print(f"More details: https://www.virustotal.com/gui/file/{file_hash}")
                break

# If no results found after waiting
if not file_check:
    print("Scan still in progress. Try again later.")
