import csv
import requests
import re
from bs4 import BeautifulSoup
import getMajorInformation

current_major = ["Physics, BS"]
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

current_requirements, current_selectives = getMajorInformation.get_info(current_major[0])

for major in college_majors:
    requirements, selectives = getMajorInformation.get_info(major)