import requests
from bs4 import BeautifulSoup
import os

def Download(stCode, stName, level):
    # URL to scrape the data from, PB is the state code for Punjab
    url = f'https://bhuvan-app1.nrsc.gov.in/state/get/layers.php?q={stCode}'

    # Send a GET request to the URL and store the response
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the div with id 'minuslevel901'. This div contains the date values we need to scrape which are listed under S-NPP VIIRS Active Agricultural Fire heading
        # If this id ever changes, we will need to update this code
        div = soup.find('div', id=level)
        
        if div:
            spans = div.find_all('span')
            # Loop through all the spans and extract the date values. each loop is one date value
            for span in spans:
                # a is the date time value
                a = span.get_text(strip=True)
                # replace space with %20 for the URL
                b = a.replace(' ', '%20')
                # replace : with _ for the file name
                c = a.replace(':', '_')
                # URL to download the XML Data for a specific date
                url = f"https://bhuvan-app1.nrsc.gov.in/state/get/createkml_agrifirecurr.php?date={b}&state={stName}"
                
                # Create the directory if it doesn't exist
                directory = os.path.join(os.getcwd(), stCode)
                if not os.path.exists(directory):
                    os.makedirs(directory)
                
                fileName = os.path.join(directory, f"{c}.csv")
                # if the file already exists, skip the download
                if os.path.exists(fileName):
                    print(f"File {fileName} already exists. Skipping download.")
                    continue
                with open(fileName, "wb") as file:
                    file_response = requests.get(url)
                    if file_response.status_code == 200:
                        content = file_response.content
                        # the file is downloaded as a KML file. We need to extract the coordinates from the KML file
                        soup_kml = BeautifulSoup(content, 'xml')
                        # find all the coordinates in the KML file
                        coordinates = soup_kml.find_all('coordinates')
                        for coordinate in coordinates:
                            file.write(coordinate.get_text(strip=True).encode('utf-8') + b'\n')
                        print(f"File {fileName} downloaded successfully.")
                    else:
                        print(f"Failed to retrieve the file for date {a}. Status code: {file_response.status_code}")
                print(a)
        else:
            print("Div with id 'minuslevel901' not found.")

    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

Download("PB","PUNJAB", "minuslevel901")
Download("UP","UTTAR%20PRADES", "minuslevel31")
Download("HR","HARYANA", "minuslevel31")
