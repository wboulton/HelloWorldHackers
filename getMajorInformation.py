import csv
import requests
import re
from bs4 import BeautifulSoup, NavigableString

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

        if logging:
            if ("college" in row.text.lower()) and ("core" in row.text.lower()) and ("Credits: " not in row.text):
                break 

            is_class = False

            if row.h3:
                text = row.h3.text

            if row.h4:
                text = row.h4.text

            if row.th:
                text = row.th.text

            if row.td and row.td.get("class") and "course" in row.td.get("class"):
                text = row.td.text
                is_class = True

            if (is_class or "Selective" in text):
                output.append(text)            

        for element in row.find_all("h3"):
            if (("Major" in element.text) or ("Minor" in element.text)) and (("Courses" in element.text) or ("Requirements" in element.text)):
                logging = True
        for element in row.find_all("h2"):
            if (("Major" in element.text) or ("Minor" in element.text)) and (("Courses" in element.text) or ("Requirements" in element.text)):
                logging = True
 
    output = [re.split(r'[^\x00-\x7F]', item)[0].strip() for item in output]

    # Split the output array into two lists based on the split line
    split_index = -1  # Initialize with -1 to indicate not found
    for i, item in enumerate(output):
        if "Selective" in item:
            split_index = i
            break  # Exit the loop once found

    if split_index == -1:
        major_requirements = output
        major_selectives = None
    else:
        number = output.count('')
        for i in range (number):
            output.remove('')
        major_requirements = output[:split_index]
        major_selectives = output[split_index:]
    return major_requirements,major_selectives
        
def find_link(search_word):
    results = ''
    
    with open("public/links.csv", mode='r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        
        for row in csvreader:
            if row and row[0] == search_word:  # Check if the first column matches the search word
                results = row[2]  # Append the last column to results

    return results

def get_info(major): 
    link = find_link(major)
    return scrape(link)

if __name__ == "__main__":
    major = "Computer Science: Software Engineering, BS"
    requirements,selectives = get_info(major)
    print(requirements)
    print(selectives)
