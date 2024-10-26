import csv
import requests
import re
from bs4 import BeautifulSoup, NavigableString

currentMajor = ["Marketing, BS"] #temporary

def scrape(url):
    # Send a GET request to the URL
    response = requests.get(url)
    response.raise_for_status()  # Check that the request was successful

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Initialize the list to store courses and required titles
    output = []

    logging = False

    for row in soup.table.contents:
        if isinstance(row, NavigableString):
            continue

        for element in row.find_all("h3"):
            if "Major Courses" in element.text:
                logging = True

        if logging:
            if row.h3:
                if "Selective" in row.h3.text:
                    break
                output.append(row.h3.text)
                continue

            if row.th:
                output.append(row.th.text)
                continue

            if row.td and "course" in row.td.get("class"):
                output.append(row.td.text)
                continue

    # Split the output array into two lists based on the split line
    split_index = -1  # Initialize with -1 to indicate not found
    for i, item in enumerate(output):
        if "Selective" in item:
            split_index = i
            break  # Exit the loop once found

    number = output.count('')
    for i in range (number):
        output.remove('')
    major_requirements = output[:split_index - 2]
    major_selectives = output[split_index - 2:]
    return major_requirements,major_selectives
        
def find_link(search_word):
    results = ''
    
    with open("public/links.csv", mode='r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        
        for row in csvreader:
            if row and row[0] == search_word:  # Check if the first column matches the search word
                results = row[2]  # Append the last column to results

    return results

requirements = []
selectives = []
for major in currentMajor:
    link = find_link(major)
    these_requirements, these_selectives = scrape(link)
    requirements.append(these_requirements)
    selectives.append(these_selectives)   

print(requirements)
print(selectives)

def get_info(major): 
    requirements = []
    selectives = []
    link = find_link(major)
    these_requirements, these_selectives = scrape(link)
    requirements.append(these_requirements)
    selectives.append(these_selectives)
    return requirements,selectives
