import csv
import requests
import re
from bs4 import BeautifulSoup

currentMajor = "Marketing, BS" #temporary

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
    split_index = output.index("Major Selectives - Choose Six (18 credits)")
    number = output.count('')
    for i in range (number):
        output.remove('')
    major_requirements = output[:split_index]
    major_selectives = output[split_index:]
    return major_requirements,major_selectives
    
def scrape2(url):
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

    # Write the filtered list of courses and titles to a text file
    with open("temporary.txt", "w") as file:
        for course in output:
            file.write(course + "\n")

    # Open the input file and read its contents
    with open('temporary.txt', 'r') as file:
        lines = file.readlines()

    # Find the index of the line to split at
    split_index = lines.index("Major Selectives - Choose Six (18 credits)\n")

    # Create the first output file with everything before the split index
    with open('majorRequirements.txt', 'w') as file1:
        file1.writelines(lines[:split_index])

    # Create the second output file with everything from the split index onward
    with open('majorSelectives.txt', 'w') as file2:
        file2.writelines(lines[split_index:])
    

def find_link(search_word):
    results = []
    
    with open("links.csv", mode='r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        
        for row in csvreader:
            if row and row[0] == search_word:  # Check if the first column matches the search word
                results.append(row[-1])  # Append the last column to results

    return results

# Assuming majorLink is defined and contains a valid string
majorLink = find_link(currentMajor)
link = majorLink[0]
print(link)
# Find the index of the first '&'
index = link.index("returnto")

if index != -1:
    # Keep everything up to the second '&'
    trimmedlink = link[:index - 1]
else:
    # If there is no second '&', keep the original link
    trimmedlink = link

print("Trimmed Major Link:", trimmedlink)


requirements, selectives = scrape(trimmedlink)
print(requirements)
print(selectives)