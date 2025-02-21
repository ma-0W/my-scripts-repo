import requests
import os
import json

os.system("color 0A")

def get_api_key():
    api_key = os.environ.get("virustotal_api_key")
    if not api_key:
        raise ValueError("API Key 'virustotal_api_key' not found. Make sure it's set in your environment variables.")
    return api_key


def check_ip(ip):
    api_key = get_api_key()
    url = "https://www.virustotal.com/api/v3/ip_addresses/{0}".format(ip)
    headers = {
        "accept": "application/json",
        "x-apikey": api_key
    }

    response = requests.get(url, headers=headers)

    try:
        return response.json()
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response"}


def main():
    while True:
        print("Enter an IP address to lookup, or type 'exit' to quit.")
        ip = input("IP Address: ").strip()
        if ip.lower() in ['exit' , 'quit']:
            break
        result = check_ip(ip)
        # Pretty print the JSON response.
        filtered_result = {
                    "IP": result.get("data", {}).get("id"),
                    "Last Analysis Stats": result.get("data", {}).get("attributes", {}).get("last_analysis_stats"),
                }
        print(json.dumps(filtered_result, sort_keys=True, indent=4))
        print("-" * 50)  # Separator for readability
8


if __name__ == '__main__':
    main()