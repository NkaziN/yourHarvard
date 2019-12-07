from cs50 import SQL
from datetime import timedelta
import csv
import json

# Connect to SQL database
db = SQL("sqlite:////home/ubuntu/project/website/yourHarvard/yourharvard_test.db")


# ONLY UNCOMMENT THIS SECTION IF YOU WANT TO READ IN ALL NEW COURSES. NOTE THE FIRST STEP!
# Clear any existing courses in table
db.execute("DELETE FROM courses;")
# Read in list of all courses
with open("courses.json") as json_file:
    courses = json.load(json_file)
    for course in range(len(courses)):
        # Progress Bar
        print(course + 1, "/ 9936")
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
        # Bypass any missing websites
        if website == "NOURL":
            website = ""
        # Bypass any missing information and reformat time
        try:
            startTime = courses[course]["classes"][0]["meetings"][0]["startTime"].lstrip("0")
            endTime = courses[course]["classes"][0]["meetings"][0]["endTime"].lstrip("0")
            time = "%s-%s" % (startTime, endTime)

            # Split into hours and minutes
            startTime = startTime.split(":")
            start = timedelta(hours = int(startTime[0]), minutes = int(startTime[1][0:2]))
            endTime = endTime.split(":")
            end = timedelta(hours = int(endTime[0]), minutes = int(endTime[1][0:2]))
            # Compute both possible durations (and strip off days)
            duration1 = (str(end - start).split(","))[-1].split(":")
            duration2 = (str(start - end).split(","))[-1].split(":")
            # Modulo any hours larger than 12 and convert minutes
            hours1 = int(duration1[0]) % 12 + float(duration1[1]) / 60
            hours2 = int(duration2[0]) % 12 + float(duration1[1]) / 60
            # Choose the minimum remaining option
            duration = min(hours1, hours2)
        except KeyError:
            time = "TBA"
            duration = "N/A"
        # Reformat days to comma seperated list
        if days == []:
            days = "TBA"
        elif days[0]["day"] == "tba":
            days = "TBA"
        else:
            tmp = []
            for day in days:
                if day["day"] == "thu":
                    tmp.append("R")
                elif day["day"] == "sun":
                    tmp.append("U")
                else:
                    tmp.append(day["day"][0].capitalize())
            days = ''.join(tmp)
        # Combine day and time
        dayTime = "%s %s" % (days, time)
        if dayTime == "TBA TBA":
            dayTime = "TBA"
        # Reformat course code to single cell
        code = "%s %s" % (catalogSubject, courseNumber)
        # Reformat instructors to commas separated list
        tmp = []
        for instructors in instructor:
            if instructors['instructorName'] == "TBA":
                tmp.append("TBA")
            elif instructors['instructorName'] == "":
                tmp.append("TBA")
            else:
                tmp.append("%s (%s)" % (instructors['instructorName'], instructors['role'].lower().capitalize()))
        instructor = ', '.join(tmp)
        # Import into SQL Database
        db.execute("INSERT INTO courses (name,code,dayTime,semester,location,instructor,school,term,description,website,courseID,classKey,sectionNumber,bracketed,classStatus,duration) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);",
                   name,code,dayTime,semester,location,instructor,school,term,description,website,courseID,classKey,sectionNumber,bracketed,classStatus,duration)


# Read in CSV file
with open("concentrations.csv", "r") as file:
    # Clear existing stored concentrations
    db.execute("DELETE FROM concentrations;")
    # Clear existing stored course requirements/exceptions
    db.execute("DELETE FROM requirements;")
    db.execute("DELETE FROM explorer;")
    # Store the list of concentration info
    concentrations = list(csv.DictReader(file))
    # Store the list of course requirements (file stream reset required)
    file.seek(0)
    all_req_courses = list(csv.reader(file))
    # Loop through concentrations
    for concentration in range(len(concentrations)):
        # Retrieve name and number of required courses
        name = concentrations[concentration]["Concentration"]
        required = concentrations[concentration]["Courses Required"]
        # Skip any blank lines
        if name == "" or required == "":
            continue
        # Import into SQL Database
        db.execute("INSERT INTO concentrations (id,name, required) VALUES (?,?,?);", concentration + 1, name, required)

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

                # Requirements table
                # If it's a list or an exception, tell them to choose a course
                if (courses[0][0] == "!" or courses[0][0] == "*" or len(courses) > 1):
                    req_name = "Choose a course from: " + ", ".join(courses).replace("!","").replace("*","")
                    db.execute("INSERT INTO requirements (course_code, conc_id, category) VALUES (?,?,?);", req_name, concentration + 1, 999)
                # Otherwise enter it as normal
                else:
                    req_name = courses[0].upper()
                    db.execute("INSERT INTO requirements (course_code, conc_id, category) VALUES (?,?,?);", req_name, concentration + 1, cell)

                # Explorer table
                for course in range(len(courses)):
                    # General exception
                    if (courses[course][0] == "!"):
                        req_name = "Any course from: " + courses[course].replace("!","")
                        db.execute("INSERT INTO explorer (course_code, conc_id, category) VALUES (?,?,?);", req_name, concentration + 1, 999)
                    # Department exception
                    elif (courses[course][0] == "*"):
                        dept_name = courses[course][1:]
                        dept_matches = db.execute("SELECT code FROM courses WHERE code LIKE ?;", dept_name + "%")
                        # Load every matching course into explorer
                        for i in range(len(dept_matches)):
                            req_name = dept_matches[i]["code"].upper()
                            db.execute("INSERT INTO explorer (course_code, conc_id, category) VALUES (?,?,?);", req_name, concentration + 1, cell)
                    # Otherwise enter it as normal
                    else:
                        req_name = courses[course].upper()
                        db.execute("INSERT INTO explorer (course_code, conc_id, category) VALUES (?,?,?);", req_name, concentration + 1, cell)

