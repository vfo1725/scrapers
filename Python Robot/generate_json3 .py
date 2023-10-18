from io import BytesIO
import json
import os
import shutil
import sys
import base64
import requests
from favicon import favicon
from PIL import Image

# Function to generate the JSON data with user input
def generate_json(id, name, url, classification):

    # Fetch the favicon URLs using the favicon package
    favicon_urls = favicon.get(url)

    # Check if any favicon URLs were found
    if favicon_urls:
        # Fetch the favicon image
        favicon_url = favicon_urls[0].url
        response = requests.get(favicon_url)
        favicon_image = response.content

        # Resize the favicon image to 128x128 pixels
        image = Image.open(BytesIO(favicon_image))
        resized_image = image.resize((128, 128))

        # Convert the resized image to bytes
        resized_favicon_image = BytesIO()
        resized_image.save(resized_favicon_image, format='PNG')
        resized_favicon_image = resized_favicon_image.getvalue()

        # Encode the resized favicon image data to base64
        encoded_favicon = base64.b64encode(resized_favicon_image).decode()
    else:
        # Favicon not found, handle the case as per your requirement
        encoded_favicon = ""


    # Create the data dictionary with the current ID and user input values
    data = {
        "id": id,
        "name": name,
        "version": "1.0.0",
        "url": url,
        "classification": classification,
        "scope": "extended",
        "clientPasswordReset": True,
        "script": [
            "function handler(e){e.stopPropagation(),e.preventDefault()}",
            "function allow(){document.getElementsByTagName('body')[0].style.background='',document.getElementsByTagName('body')[0].style.opacity=1,document.removeEventListener('click',handler,!0)}",
            "function block(){document.getElementsByTagName('body')[0].style.background='#58595b',document.getElementsByTagName('body')[0].style.opacity=.1,document.addEventListener('click',handler,!0)};block();",
            "",
            "var x = document.evaluate('Xpath', document, null, XPathResult.ANY_TYPE, null).iterateNext(); x.value = '${username}'; x.dispatchEvent(new Event('input', {bubbles: true})); x.dispatchEvent(new Event('change', {bubbles: true}));",
            "",
            "var y = document.evaluate('Xpath', document, null, XPathResult.ANY_TYPE, null).iterateNext(); y.value = '${password}'; y.dispatchEvent(new Event('input', {bubbles: true})); y.dispatchEvent(new Event('change', {bubbles: true}));",
            "",
            "allow(); document.evaluate('XPath', document, null, XPathResult.ANY_TYPE, null).iterateNext().click();"
        ],
        "additionalScripts": [
            {
                "name": "passwordChangeFirstStep",
                "steps": []
            }
        ],
        "preElements": [],
        "successElements": [],
        "methods": [],
        "additionalProperties": {
            "logout": [""],
            "timeout": 720,
            "icon": ""
        },
        "logo": "example_logo.png"
    }


    data["additionalProperties"]["icon"] = encoded_favicon

    return data





# Generate JSON data and write to file
def generate_and_write_json(id, name, url, classification):
    data = generate_json(id, name, url, classification)

    # Serialize data to JSON
    json_data = json.dumps(data, indent=4)

    # Write JSON data to a file
    file_path = f"{name}.json"

    # Specify the file path in the Downloads directory
    downloads_directory = os.path.join(os.path.expanduser("~"), "Downloads")
    file_path = os.path.join(downloads_directory, file_path)

    with open(file_path, "w") as file:
        file.write(json_data)

    print(f"JSON file for ID {data['id']}, {data['name']} created successfully.")

    # Upload the JSON file to the destination directory
    upload_json(file_path, downloads_directory)


# Upload JSON file to a directory
def upload_json(file_path, destination_directory):
    shutil.move(file_path, destination_directory)
    print(f"JSON file '{file_path}' uploaded to '{destination_directory}' successfully.")


# Check if user input is provided for name, url, and classification
if len(sys.argv) == 5:
    id = int(sys.argv[1])
    name = sys.argv[2]
    url = sys.argv[3]
    classification = sys.argv[4]
else:
    id = int(input("Enter ID: "))
    name = input("Enter name: ")
    url = input("Enter URL: ")
    classification = input("Enter classification: ")

# Generate and write JSON data to the file
generate_and_write_json(id, name, url, classification)

