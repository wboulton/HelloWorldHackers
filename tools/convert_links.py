import requests
import re
import csv
from bs4 import BeautifulSoup

rows = []
with open("public/linksUltraCleaned.csv", newline="") as file:
    reader = csv.DictReader(file)
    for row in reader:
        rows.append(row)

for row in rows:
    row["url"] = row["url"].replace("preview_program.php", "preview_degree_planner.php")
    """
    print("Old", row["url"])
    response = requests.get(row["url"])
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    url = None

    for element in soup.find_all("a", title="Print Degree Planner (opens a new window)"):
        onclick = element["onclick"]
        if not onclick.startswith("acalogPopup('"):
            continue

        onclick = onclick[13:]
        onclick = onclick[:onclick.index("'")]
        url = "https://catalog.purdue.edu/" + onclick
        print("New", url)
        row["url"] = url
        break
    """

with open("public/links.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["name", "college", "url"])
    writer.writeheader()
    for row in rows:
        writer.writerow(row)

