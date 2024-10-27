import csv
import requests
import re
from bs4 import BeautifulSoup
import getMajorInformation

current_major = ["Computer Science: Security, BS"]
college_majors = []

def find_college(search_word):
    results = ''
    
    with open("public/links.csv", mode='r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        
        for row in csvreader:
            if row and row[0] == search_word:  # Check if the first column matches the search word
                results = row[1]  # Append the last column to results

    return results

def find_majors(college, college_majors):
    with open("public/links.csv", mode='r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        
        for row in csvreader:
            if row and college in row[1]:  # Check if the first column matches the search word
                college_majors.append(row[0])
    return college_majors
                
def compare(current_major):
    college_majors = []
    college = find_college(current_major[0])    
    college_majors = find_majors(college, college_majors)
    current_requirements = []
    current_selectives = []
    for major in current_major:
        requirements, selectives = getMajorInformation.get_info(major)
        for requirement in requirements:
            if requirement in current_requirements:
                continue
            current_requirements.append(requirement)
        
        if selectives:
            for selective in selectives:
                if selective in current_selectives:
                    continue
                current_selectives.append(selective)

    major_similarity = []
    for major in college_majors:
        i = 0
        print(major)
        requirements, selectives = getMajorInformation.get_info(major)
        for course in requirements:
            if (course in current_requirements) or (course in current_selectives):
                continue
            if not " or " in course:
                i += 1
        k = 0
        selectives_required = 0
        if selectives:
            match = re.search(r'\d+', selectives[0][0])
            if match:
                selectives_required = int(match.group()) / 3
            else:
                selectives_required = 0
            for course in selectives:
                if (course in current_requirements) or (course in current_selectives):
                    continue
                if k >= selectives_required:
                    break
                k += 1
        major_similarity.append([major, k+i])

    sorted_data = sorted(major_similarity, key=lambda x: x[1])
    if "Computer Science: Security, BS" in current_major:
        sorted_data.insert(0, "lock in my guy!")
    return sorted_data
    
if __name__ == '__main__':
    data = compare(["Computer Science: Security, BS"])
    print(data)
