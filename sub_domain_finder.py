import requests
from requests.auth import HTTPBasicAuth
import argparse

# Function to scrape structured scopes for each username
def scrape_structured_scopes(username, password, input_file, output_file):
    # Base URL for structured scopes
    base_url = "https://api.hackerone.com/v1/hackers/programs/{}/structured_scopes"
    headers = {
        "Accept": "application/json"
    }

    # Open the output file for writing
    with open(output_file, 'w') as outfile:
        # Open the input file to read usernames
        with open(input_file, 'r') as infile:
            usernames = infile.read().splitlines()

            # Iterate over each username
            for user in usernames:
                # Format the URL with the current username
                url = base_url.format(user.strip())
                
                # Make the request with Basic Authentication
                response = requests.get(url, headers=headers, auth=HTTPBasicAuth(username, password))

                # Check if the request was successful
                if response.status_code == 200:
                    scopes_data = response.json()

                    # Check if structured scopes are present
                    if 'data' in scopes_data and scopes_data['data']:
                        for scope in scopes_data['data']:
                            asset_type = scope['attributes'].get('asset_type', 'N/A')
                            asset_identifier = scope['attributes'].get('asset_identifier', 'N/A')
                            eligible_for_bounty = scope['attributes'].get('eligible_for_bounty', 'N/A')

                            # Print scope information
                            print(f"\033[94mUser: {user.strip()}, Asset Type: {asset_type}, Asset Identifier: {asset_identifier}, Eligible for Bounty: {eligible_for_bounty}\033[0m")  # Print in blue

                            # Check if eligible for bounty and asset type is URL
                            if eligible_for_bounty and asset_type.lower() == 'url':
                                # Write only the asset identifier to the output file
                                outfile.write(f"{asset_identifier}\n")
                    else:
                        print(f"\033[91mNo structured scopes found for {user.strip()}\033[0m")  # Print in red
                else:
                    print(f"\033[91mError fetching data for {user.strip()}: {response.status_code} - {response.text}\033[0m")

# Main function to handle command-line arguments
def main():
    parser = argparse.ArgumentParser(
        description='This script will take organization handle names and give eligible asset identifiers in bounty scopes.'
    )
    parser.add_argument('-f', '--flag', required=True, help='Username and password in the format user:pass')
    parser.add_argument('-i', '--input', required=True, help='Input file containing organization handle names')
    parser.add_argument('-o', '--output', required=True, help='Output file to save eligible asset identifiers')

    # Parse the arguments
    args = parser.parse_args()

    # Split the user:pass string
    try:
        username, password = args.flag.split(':')
    except ValueError:
        print("Error: Please provide credentials in the format user:pass")
        return

    # Call the scrape function with provided credentials, input file, and output file
    scrape_structured_scopes(username, password, args.input, args.output)

if __name__ == '__main__':
    main()
