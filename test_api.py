import requests
import json
import os

# Define the URL of your Flask API's predict endpoint
url = 'http://127.0.0.1:5000/predict'

# Define the full, absolute path to the image file you want to send.
# This path is hardcoded to the location where your image is currently stored.
file_path = "Nazreen-Khan-is-a-Homemaker-from-Bally-Census_yyth_jpg.rf.84c908f5a30ee78298f1d4881226fd84.jpg"

try:
    # Check if the file exists at the specified path
    if not os.path.exists(file_path):
        print(f"Error: File not found at '{file_path}'")
    else:
        # Open the image file in binary read mode
        with open(file_path, 'rb') as f:
            # Prepare the files dictionary for the POST request
            # 'file' is the key name that your Flask API expects (request.files['file'])
            files = {'file': f}
            
            # Send the POST request to the API
            response = requests.post(url, files=files)
            
            # Check if the request was successful
            if response.status_code == 200:
                print("Request successful!")
                print("--- API Response ---")
                
                # Pretty print the JSON response
                try:
                    response_json = response.json()
                    print(json.dumps(response_json, indent=4))
                except json.JSONDecodeError:
                    print("Could not decode JSON response.")
                    print("Raw response content:")
                    print(response.content.decode())
            else:
                print(f"Request failed with status code: {response.status_code}")
                print(f"Response: {response.text}")
                
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
