from cs50 import SQL
import sys
import csv
import json

"""WARNING: THIS SCRIPT TAKES A VERY LONG TIME TO RUN AND CLEARS THE COURSES TABLE"""

# Connect to SQL database
db = SQL("sqlite:///yourharvard.db")

# Clear any existing courses in table
db.execute("DELETE FROM courses;")
# Read in list of all courses
with open("courses.json") as json_file:
    courses = json.load(json_file)
    for course in range(len(courses)):
        # Progress Bar
        print(course+1, "/ 9936")
        # Retrieve all course information
        courseID = courses[course]["courseID"]
        classKey = courses[course]["classes"][0]["classKey"]
        semester = courses[course]["classes"][0]["term"]
        term = courses[course]["classes"][0]["session"]
        sectionNumber = courses[course]["classes"][0]["sectionNumber"]
        bracketed = courses[course]["classes"][0]["bracketed"]
        school = courses[course]["classes"][0]["catalogSchool"]
        catalogSubject = courses[course]["classes"][0]["catalogSubject"]
        classStatus = courses[course]["classes"][0]["classStatus"]
        description = courses[course]["classes"][0]["courseDescription"]
        courseNumber = courses[course]["classes"][0]["courseNumber"]
        name = courses[course]["classes"][0]["courseTitle"]
        website = courses[course]["classes"][0]["courseWebsite"]
        location = courses[course]["classes"][0]["meetings"][0]["publishedLocation"]
        days = courses[course]["classes"][0]["meetings"][0]["days"]
        instructor = courses[course]["classes"][0]["meetings"][0]["publishedInstructors"]
        # Bypass any missing information
        try:
            startTime = courses[course]["classes"][0]["meetings"][0]["startTime"]
            endTime = courses[course]["classes"][0]["meetings"][0]["endTime"]
        except KeyError:
            startTime = "TBA"
            endTime = "TBA"
        # Reformat course code to single cell
        code = "%s %s" % (catalogSubject, courseNumber)
        # Reformat days to comma seperated list
        if days == []:
            days = "TBA"
        elif days[0]["day"] == "tba":
            days = "TBA"
        else:
            tmp = []
            for day in days:
                tmp.append(day["day"].capitalize())
            days = ', '.join(tmp)
        # Reformat instructors to commas separated list
        tmp = []
        for instructors in instructor:
            tmp.append("%s (%s)" % (instructors['instructorName'], instructors['role'].lower().capitalize()))
        instructor = ', '.join(tmp)
        # Import into SQL Database
        db.execute("INSERT INTO courses (name,code,days,semester,startTime,endTime,location,instructor,school,term,description,website,courseID,classKey,sectionNumber,bracketed,classStatus) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);",
                   name, code, days, semester, startTime, endTime, location, instructor, school, term, description, website, courseID, classKey, sectionNumber, bracketed, classStatus)
