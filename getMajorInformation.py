import csv
import requests
import re
from bs4 import BeautifulSoup

currentMajor = ["Marketing, BS"] #temporary

def scrape(url):
    # Send a GET request to the URL
    response = requests.get(url)
    response.raise_for_status()  # Check that the request was successful

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Initialize the list to store courses and required titles
    output = []

    for element in soup.find_all("div"):
        if element.h2 and "Major Courses" in element.h2.text:
            sections = element.next_sibling.children

    for section in sections:
        output.append(section.h3.text)
        output.append("")
        for element in section.find_all("li"):
            text = element.text
            if len(text) == 1:
                continue
            if element.a:
                text = element.a.text
            elif " -" in text:
                text = text[:text.index(" -")]
            
            if text[-1] == " ":
                text = text[:-1]
            
            output.append(text)
        output.append("")

    # Split the output array into two lists based on the split line
    split_index = -1  # Initialize with -1 to indicate not found
    for i, item in enumerate(output):
        if "Selective" in item:
            split_index = i
            break  # Exit the loop once found

    if split_index != -1:
        print(f"'Major Selectives' found at index: {split_index}")
    else:
        print("'Major Selectives' not found in the output.")
    number = output.count('')
    for i in range (number):
        output.remove('')
    major_requirements = output[:split_index - 2]
    major_selectives = output[split_index - 2:]
    return major_requirements,major_selectives
        
def find_link(search_word):
    results = ''
    
    with open("public/linksUltraCleaned.csv", mode='r', newline='', encoding='utf-8') as csvfile:
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
