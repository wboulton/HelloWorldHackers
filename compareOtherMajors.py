import csv
import requests
import re
from bs4 import BeautifulSoup
import getMajorInformation

current_major = ["Marketing, BS"]
college_majors = []

def find_college(search_word):
    results = ''
    
    with open("public/linksUltraCleaned.csv", mode='r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        
        for row in csvreader:
            if row and row[0] == search_word:  # Check if the first column matches the search word
                results = row[1]  # Append the last column to results

    return results

def find_majors(college):
    with open("public/linksUltraCleaned.csv", mode='r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        
        for row in csvreader:
            if row and college in row[1]:  # Check if the first column matches the search word
                college_majors.append(row[0])
                

college = find_college(current_major[0])    
find_majors(college)

current_requirements = []
current_selectives = []
for major in current_major:
    requirements, selectives = getMajorInformation.get_info(major)
    for requirement in requirements:
        if requirement in current_requirements:
            continue
        current_requirements.append(requirement)
        
    for selective in selectives:
        if selective in current_selectives:
            continue
        current_selectives.append(selective)

major_similarity = []
for major in college_majors:
    i = 0
    print(major)
    requirements, selectives = getMajorInformation.get_info(major)
    for course in requirements[0]:
        if (course in current_requirements) or (course in current_selectives):
            print(course, current_requirements,current_selectives)
            continue
        i += 1
    k = 0
    selectives_required = 0
    match = re.search(r'\d+', selectives[0][0])
    if match:
        selectives_required = int(match.group()) / 3
    else:
        selectives_required = 0
    for course in selectives[0]:
        if (course in current_requirements) or (course in current_selectives):
            print(course, current_requirements,current_selectives)
            continue
        if k > selectives_required:
            break
        k += 1
    major_similarity.append([major, k+i])

sorted_data = sorted(major_similarity, key=lambda x: x[1])

print(sorted_data)