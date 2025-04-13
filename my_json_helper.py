import json
import os
import pandas as pd 

def read_json_file_to_dataframe(file_path):
    """
    Read a JSON file and convert it to a pandas DataFrame

    Args:
        file_path (str): The path to the JSON file
    Returns:
        pd.DataFrame: A DataFrame containing the data from the JSON file
    """
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        df = pd.DataFrame(data['results'])
        return df
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error
    
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