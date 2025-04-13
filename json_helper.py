import urllib.request
import urllib.error  # For handling HTTP and URL errors
# This script demonstrates how to make a GET request to an API using Python's urllib library.
# It includes error handling for common issues like HTTP errors and URL errors.
# The script retrieves data from the NOAA Climate Data Online API and parses the JSON response.
# The script is designed to be run as a standalone program, but the main functionality is encapsulated in the call_api function.
# The script uses the urllib library to make HTTP requests and handle responses.
# The script is designed to be run as a standalone program, but the main functionality is encapsulated in the call_api function.
import json
import os
import pandas as pd 

web_site = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&locationid=FIPS:10003&startdate=2018-01-01&enddate=2018-01-31'
token = 'UHXohzHdhMmtTMDEsZrzsNJYqXsORDFt'

def call_api(url, token):
    """
    Make a GET request to the API and return a JSON response

    Args:
        url (str): The API endpoint URL
        token (str): The API token for authentication
    Returns:
        dict: The parsed JSON response from the API
    Summary of What Happens
    1. A Request object is created for the URL.
    2. A custom header (token) is added to the request.
    3. The request is sent to the server using urlopen.
    4. The server's response is read, decoded from bytes to a string, and parsed as JSON.
    5. The resulting Python object (data) contains the parsed JSON data.
    """
    try:
        req = urllib.request.Request(url)
        req.add_header('token', token)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            # Get the remaining rate limit from the headers
            rate_limit_remaining = int(response.headers.get('X-RateLimit-Remaining', 0))
            return data, rate_limit_remaining

    except urllib.error.HTTPError as e:
        # Handle HTTP errors (e.g., 404, 401)
        print(f"HTTP Error: {e.code} - {e.reason}")
    except urllib.error.URLError as e:
        # Handle URL errors (e.g., network issues)
        print(f"URL Error: {e.reason}")
    except json.JSONDecodeError as e:
        # Handle JSON parsing errors
        print(f"JSON Decode Error: {e.msg}")
    except Exception as e:
        # Handle any other unexpected errors
        print(f"An unexpected error occurred: {e}")

    return None,0  # Return None if an error occurs

def save_json_to_file(data, filename):
    """
    Save JSON data to a file

    Args:
        data (dict): The JSON data to save
        filename (str): The name of the file to save the data to
    """
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4) # Pretty print the JSON, the indentation level is 4 spaces
            print(f'Data saved to {filename}')
    except IOError as e:
        # Handle file I/O errors
        print(f'File I/O Error: {e}')
    except Exception as e:
        # Handle any other unexpected errors
        print(f'An unexpected error occurred while saving the file: {e}')

# implement me
def read_all_json_files_to_dataframe(file_path):
    json_files = pd.DataFrame()  # create an empty DataFrame
    # Loop through all files in the file_path directory
    for files in os.listdir(file_path):
        full_path = os.path.join(file_path, files)

        try:
            with open(full_path, 'r') as f:
                data = json.load(f)
            json_df = pd.DataFrame(data['results'])
            # Add a 'source' column to track the file name
            json_df['source'] = files
            # concat the DataFrame to the json_files DataFrame
            json_files = pd.concat([json_files, json_df], ignore_index=True)
        except Exception as e:
            print(f"Error reading {full_path}: {e}")
    
    return json_files

if __name__ == '__main__':
    limit = 1000  # The maximum number of records to retrieve in one request
    initial_offset = 1  # Start the offset at 1

    for i in range(2):  # Loop twice for 2 API calls
        offset = initial_offset + (i * limit)  # Calculate the offset dynamically
        url = f"{web_site}&limit={limit}&offset={offset}"  # Construct the URL
        output_file = f"daily_summaries_FIPS10003_jan_2018_{i}.json"  # Name the output file

        print(f"Calling API with: {url}")
        response, remaining_requests = call_api(url, token)

        # Check if the response is valid
        if response:
            results = response.get('results', [])
            print(f"Fetched {len(results)} records in this batch.")

            # Save the response to a file
            save_json_to_file(response, output_file)
            print(f"Data saved to {output_file}")

            # Stop if fewer records are returned than the limit
            if len(results) < limit:
                print("No more records to fetch.")
                break
        else:
            print(f"Failed to retrieve data for offset {offset}, exiting loop.")
            break

