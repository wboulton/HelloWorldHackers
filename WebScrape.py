import requests
import re
from bs4 import BeautifulSoup

# URL of the page to scrape
url = "https://catalog.purdue.edu/preview_program.php?catoid=17&poid=29812&hl=%22Physics%22&returnto=search"

# Send a GET request to the URL
response = requests.get(url)
response.raise_for_status()  # Check that the request was successful

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Initialize the list to store courses and required titles
courses = []

# Find all text in <li> and <strong> elements
for element in soup.find_all("div"):
    if element.h2 and "Major Courses" in element.h2.text:
        major_courses = element.next_sibling

for element in major_courses.find_all("li"):
    courses.append(element.text)

# Write the filtered list of courses and titles to a text file
with open("majorData.txt", "w") as file:
    for course in courses:
        file.write(course + "\n")
