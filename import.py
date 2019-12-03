from cs50 import SQL
import sys
import csv

# Confirm the correct number of arguments
if len(sys.argv) is not 2:
    print("Usage: python import.py filename.csv")
    sys.exit()
# Connect to SQL database
db = SQL("sqlite:///yourharvard.db")

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


# Read in CSV file
with open(sys.argv[1], "r") as file:
    # Clear existing stored concentrations
    #db.execute("DELETE FROM concentrations;")
    # Store all of the general concentration info (first few columns)
    concentrations = list(csv.DictReader(file))
    # Store the list of course requirements (file stream reset required)
    #file.seek(0)
    #req_courses = list(csv.reader(file))
    # Loop through concentrations
    for concentration in range(len(concentrations)):
        """
        # Retrieve name and number of required courses
        name = concentrations[concentration]["Concentration"]
        required = concentrations[concentration]["Courses Required"]
        # Import into SQL Database
        db.execute("INSERT INTO concentrations (id,name, required) VALUES (?,?,?);", concentration + 1, name, required)
        """
        # Retrieve list of course requirements (from course header to first blank)
        start = courses[0].index("Courses")
        end = courses[concentration + 1].index("")
        course_list = courses[concentration + 1][start:end]
        # Import into SQL database
        category = 0
        for course in range(len(course_list)):
            # Split by comma if multiple courses are accepted
            course = course_list[course].split(",")
            # Insert all courses into requirements or exceptions database
            for i in range(len(course)):
                if course[i][0] = "!"
                    ##Insert into exceptions
                else:
                    ##db.execute("INSERT INTO requirements (course_id, conc_id, category) VALUES (?,?,?);", __________, concentration + 1, category)
            # Update category number
            category += 1
            print(course)