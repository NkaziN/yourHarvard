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
    """
    # Clear existing stored concentrations
    db.execute("DELETE FROM concentrations;")
    """
    # Clear existing stored course requirements/exceptions
    db.execute("DELETE FROM requirements;")
    db.execute("DELETE FROM exceptions;")
    # Store the list of concentration info
    concentrations = list(csv.DictReader(file))
    # Store the list of course requirements (file stream reset required)
    file.seek(0)
    all_req_courses = list(csv.reader(file))
    # Loop through concentrations
    for concentration in range(4):#len(concentrations)):
        # Stop at the blank line
        if concentrations[concentration] == "":
            sys.exit()
        """
        # Retrieve name and number of required courses
        name = concentrations[concentration]["Concentration"]
        required = concentrations[concentration]["Courses Required"]
        # Import into SQL Database
        db.execute("INSERT INTO concentrations (id,name, required) VALUES (?,?,?);", concentration + 1, name, required)
        """
        # Retrieve list of course requirements (from course header to first blank)
        print(concentrations[concentration]["Concentration"])
        start = all_req_courses[0].index("Courses")
        # Avoids error when no empty cell exists
        try:
            end = all_req_courses[concentration + 1].index("")
            cell_list = all_req_courses[concentration + 1][start:end]
        except ValueError:
            cell_list = all_req_courses[concentration + 1][start:]

        # Import into SQL database
        # Each cell in the list contains 1+ courses
        for cell in range(len(cell_list)):
            if (cell_list[cell] == ""):
                continue
            else:
                # Split by comma in case courses are in cell
                courses = cell_list[cell].split(", ")
                for course in range(len(courses)):
                    # Check for a general exception (first cell element is !)
                    if (courses[course][0] == "!"):
                        exception_name = courses[course][1:]
                        db.execute("INSERT INTO exceptions (conc_id, name, category) VALUES (?,?,?);", concentration + 1, exception_name, cell)
                    # Department exception
                    elif (courses[course][0] == "*"):
                        dept_name = courses[course][1:]
                        dept_matches = db.execute("SELECT code FROM courses WHERE code LIKE ?;", dept_name + "%")
                        # Load every matching course into requirements
                        for i in range(len(dept_matches)):
                            req_name = dept_matches[i]["code"].upper()
                            db.execute("INSERT INTO requirements (course_code, conc_id, category) VALUES (?,?,?);", req_name, concentration + 1, cell)
                    # Enter the course as normal
                    else:
                        req_name = courses[course].upper()
                        db.execute("INSERT INTO requirements (course_code, conc_id, category) VALUES (?,?,?);", req_name, concentration + 1, cell)