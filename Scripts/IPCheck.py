import requests
import os
import json


def get_api_key():
    api_key = os.environ.get("abuse_ip_db")
    if not api_key:
        raise ValueError("API Key 'abuse_ip_db' not found. Make sure it's set in your environment variables.")
    return api_key

token = get_api_key()

def main():
    # Defining the api-endpoint
    api_base = 'https://api.abuseipdb.com/api/v2/check'

    ipAddress = input("Please enter an IP address to lookup: ")

    querystring = {
        'ipAddress': ipAddress,
        'maxAgeInDays': '90'

    }

    headers = {
        'Accept': 'application/json',
        'Key': token
    }

    response = requests.request(method='GET', url=api_base, headers=headers, params=querystring)

    # Formatted output
    decodedResponse = json.loads(response.text)
    print(json.dumps(decodedResponse, sort_keys=True, indent=4))

main()