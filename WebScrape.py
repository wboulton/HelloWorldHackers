import requests
import re
from bs4 import BeautifulSoup

# URL of the page to scrape
url = "https://catalog.purdue.edu/preview_program.php?catoid=17&poid=29755&hl=%22marketing+BS%22&returnto=search"

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
with open("output.txt", "w") as file:
    for course in output:
        file.write(course + "\n")

