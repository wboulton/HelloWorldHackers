import requests
import csv
from bs4 import BeautifulSoup

url = "https://catalog.purdue.edu/content.php?catoid=17&navoid=22229"

response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'html.parser')

output = []

for element in soup.find_all("h2"):
    if element.text == "Purdue University":
        root_div = element.next_sibling.next_sibling
        break

colleges = {}

for element in root_div.children:
    if element.name == "h3":
        college = element.text.strip()
        div = element.next_sibling.next_sibling
        if div and div.name == "div":
            colleges[college] = div

for college, div in colleges.items():
    for element in div.find_all("li"):
        if not element.a:
            continue
        element = element.a
    
        name = element.text
        url = "https://catalog.purdue.edu/" + element["href"]
        output.append({"name": name, "college": college, "url": url})

with open("links.csv", "w") as file:
    writer = csv.DictWriter(file, fieldnames=["name", "college", "url"])
    writer.writeheader()
    for program in output:
        writer.writerow(program)

