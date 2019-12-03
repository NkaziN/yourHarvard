from cs50 import SQL
import sys
import csv
import json

"""
# Confirm the correct number of arguments
if len(sys.argv) is not 2:
    print("Usage: python import.py filename.csv")
    sys.exit()

# Connect to SQL database
db = SQL("sqlite:///yourharvard.db")
"""

with open("courses.json") as json_file:
    data = json.load(json_file)
    print(data[0])

"""
ONLY UNCOMMENT THIS SECTION IF YOU WANT TO READ IN ALL NEW COURSES. NOTE THE FIRST STEP!
# Read in list of all courses
with open("undergrad.csv", "r") as file:
    # Clear any existing courses in table
    db.execute("DELETE FROM courses;")
    # Store all of the course information
    courses = list(csv.DictReader(file))
    for course in range(len(courses)):
        # Retrieve all course information
        name = courses[course]["Name"]
        code = courses[course]["Code"]
        instructor = courses[course]["Instructor"]
        school = courses[course]["School"]
        department = courses[course]["Department"]
        semester = courses[course]["Semester"]
        term = courses[course]["Term"]
        time = courses[course]["Time"]
        description = courses[course]["Description"]
        # Import into SQL Database
        db.execute("INSERT INTO courses (name,code,instructor,school,department,semester,term,time,description) VALUES (?,?,?,?,?,?,?,?,?);", name, code, instructor, school, department, semester, term, time, description)
"""
