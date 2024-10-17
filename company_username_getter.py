import requests
from requests.auth import HTTPBasicAuth
import argparse

# Function to scrape programs and bounties
def scrape_programs(username, password, output_file, page_size, page_number):
    url = f"https://api.hackerone.com/v1/hackers/programs?page[size]={page_size}&page[number]={page_number}"
    headers = {
        "Accept": "application/json"
    }

    # Make the request with Basic Authentication
    response = requests.get(url, headers=headers, auth=HTTPBasicAuth(username, password))

    # Check if the request was successful
    if response.status_code == 200:
        programs_data = response.json()

        # Open the file for appending
        with open(output_file, 'a') as file:
            # Iterate over each program and check if bounties are offered
            for program in programs_data['data']:
                program_handle = program['attributes']['handle']
                offers_bounties = program['attributes'].get('offers_bounties', False)

                # If the program offers bounties, print and write only the program handle to the file
                if offers_bounties:
                    print(f"\033[94m{program_handle}\033[0m")
                    file.write(f"{program_handle}\n")
                else:
                    # Print in red if the program does not offer bounties
                    print(f"\033[91m{program_handle} does not offer bounties\033[0m")
    else:
        print(f"Error: {response.status_code} - {response.text}")

# Main function to handle command-line arguments
def main():
    parser = argparse.ArgumentParser(description='Scrape program handles that offer bounties from HackerOne')
    parser.add_argument('-f', '--flag', required=True, help='Username and password in the format user:pass')
    parser.add_argument('-o', '--output', required=True, help='Output file to save program handles offering bounties')
    parser.add_argument('--page-size', type=int, default=100, help='Number of programs per page (default: 100)')
    parser.add_argument('--page-number', type=int, default=1, help='Page number to retrieve (default: 1)')
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Split the user:pass string
    try:
        username, password = args.flag.split(':')
    except ValueError:
        print("Error: Please provide credentials in the format user:pass")
        return

    # Call the scrape function with provided credentials, output file, page size, and page number
    scrape_programs(username, password, args.output, args.page_size, args.page_number)

if __name__ == '__main__':
    main()
