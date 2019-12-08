# yourHarvard



# Importing myHarvard Course Information (courses table)
Since the project is a course planner, it relies heavily on course information. We approached this in two ways.
First, we developed a program to log into my.harvard and manually retrieve course information. Though simply logging into
a website from the command line is rather straightforward, bypassing Duo Two-Factor Authentication proved to be a challenge.
The scraper gets around this using selenium, a web browser driver, which allows the user to manually login on a visual browser
before scraping data. We wanted to make the process as automated as possible, so the user can enter their username, password,
and the number of pages to scrape directly into the top of the script. After submitting the user's login info, the program
waits at the authentication page for the user to manually enter the Duo Authentication code or respond to a push. Afterwards,
the page visits the URL matching the search query for all FAS courses. HUIT passes the page number via GET, which makes it
easy to increment the page by changing the URL. After visiting each page, the program retrieves all data and immediately writes
it to file. This ensures that the data is stored, even if there is an error later on. Since the program is continually writing
more course data, the export is set to append, rather than "w+". File encoding is done in utf-8 since certain Arabic courses
have non-ASCII characters in their course descriptions, leading to errors. This program is still preserved in the /scraper
folder, but has since been retired in favor of the json provided by CS50.

We store course data using import_all.py and n is the first portion of the script. Typically, new imports go directly to a
test database, so multiple people can continue using the site as data is updated. After reading in course information, every
single piece of data stored in the json is retrieved for each course (even data that is not currently being utilized for
some functionality). As data is retrieved for each course, the progress is printed to terminal for easy monitoring. After all
fields have been retrieved, a few undergo further processing. The website field replaces "NOURL" with an empty string, to make
it easy to identify which courses are lacking a site. This allows us to merely ask whether website == NULL, rather than
specifying a string. The course times are reformatted for easy readability (rather than leaving them as "startTime" and
"endTime"), which makes the HTML code simpler. The duration calculation is rather involved. After separating the times into
hours and minutes, the times are subtracted from one another in both directions. The resulting times are modulod by 12, and
the smallest value is saved as the course duration. If any time information is missing, both the times and duration are
saved as TBA.

We chose to do a significant amount of manipulation in python to simplify the HTML code as much as possible. For example,
the times are converted into the desired display format in python, to avoid potential errors due to missing data.
Similarly, the duration calculation is much easier to determine in python, so after completion, it is stored in the
table in the same format we want it to display in.We also wanted to convert the days each course is offered to a one letter code, so after extracting the initial letter
(with the exception of Thu/Sun), we create a string of days the course is offered. This is attached to the times
from above and stored directly in the display format.

We found it simpler to refer to courses using their course code throughout the project, so all course data was saved
relative to the code. This required combining fields from the courses json.

The instructor field was easiest to view as a comma separated list, so we reformatted the table as the desired display format.

The description field had leftover HTML tags which we attempted to clean up. Using a regular expression, we removed
the tags themselves (<>) but there were several HTML entities such as "&nbsp;" leftover. We attempted to replace
several of the most common entities with the item they referenced according to w3schools.com/html/html_entities.asp.
However, we couldn't get everything. Rather than poring through every single description in the database, we added
a catchall, by removing any leftover entities (rather than replacing them).

Finally, we stored everything in a single, massive courses database, allowing us to access all of the data for each
course. Since we saved information in the same way that we wanted it to display for the course, only one table was
necessary.

# Importing Concentration Information (concentration, requirements, and explorer tables)
First, we had to retrieve the required courses for every concentration. This task was done manually, and the courses
and concentration names were entered into a csv file. The syntax of the csv file is as follows:
Each row refers to one concentration. Concentration name and the number of required courses are plaintext.
Each cell refers to a different requirement. If multiple courses fulfill a requirement, they go in one cell with comma separation.
Sometimes a requirement is vague, rather than a specific course. This is indicated by a ! before the text
Sometime a requirement calls for a whole department. This is indicated by a * before the department name

Concentrations Table
This information was all stored as plaintext in the csv, and easily accessible from the concentration sites. It was stored with
no additional processing. Spaces were stripped from the ends of the name to avoid entry errors.

Requirements Table
This is the table used for the scheduling page. After processing, we want each cell to become a single card for easy
readability. If a single course meets a requirement (one course in the cell), we store it by its course code. However,
if the requirement is vague or several courses can satisfy a requirement, we store a list of possible options. This
is saved in the "course code" field since we want it to display, even though it's not actually a course code.

Explorer Table
This is the table used for the course explorer page. After processing, we want to show every single course that may
count toward a concentration. This means we want to parse a list of courses and show each one individually. We do this
by inserting courses normally, inserting exceptions using the same ! flag, and parsing when we see the * flag indicating a
department. For instance, when we see "*MCB", we pull every single MCB course from the courses database and insert
them as new cards. This would be visually overwhelming for the schedule page, but it's just right for the course explorer.

# Login/Register
These pages worked similarly to finance, but we didn't want to redirect users to an apology page. Instead, users are
redirected to the same page, but the placeholder text updates to indicate that a field is missing, username is taken,
etcetera.

# Schedule Page
The schedule page is the core functionality of our proposal. Once the user submits a concentration name, the program
retrieves all course data for the courses required for the concentration (by joining the courses and requirements tables)
and returns it to the html page. The schedule goes through the process of generating a new html card for each course,
populating it with the course information. Courses with a website also get a footer linking to the course page.

In addition to the courses in the requirement table, there are several entries that correspond to a list rather than
an individual course. This occurs when multiple courses satisfy one requirement (multiple courses in one cell).
After the standard course cards are generated, the page generates elective cards containing each list. Since the lists
don't correspond to elements in the courses table, the only data passed is the list contents (stored as the course code).
Since the for loop for the elective card generation is after the standard course cards, all of the electives are at
the bottom of the page, while the standard cards are on top.

These cards can be dragged onto the table, which is a labeled container storing div elements. This means the table
will resize dynamically as items are added.

We realized that people may want to edit the course cards, to add new details, or the elective cards, to specify
which course they actually plan on taking. For this reason, the card bodies were made editable in CSS.


# Course Explorer
The course explorer page is intended to show (a nonexhaustive list of) courses that  count toward a concentration
based on the website. Similarly to the schedule page, after a concentration is entered, all relevant course information
is retrieved via SQL query. Also, the title bar changes to "Explore {{concentration name}}" which is a little
more friendly, and the current concentration name and number of courses are retrieved via SQL query.

Since the page is intended to show all courses that meet a concentration requirement, cards are of a fixed width.
This ensures that the page is visually consistent and courses appear in neat rows. Again, the course cards are
generated first, and the electives appear that the end of the list, since users are likely most interested in
courses.

The sheer number of courses can make this page overwhelming, so the current card will change color on hover. This
ensures that you always can find your mouse pointer, and it's obvious where your attention should be. Each card
also features an HTML details field that displays a short course description.

