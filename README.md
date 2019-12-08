# yourHarvard

# Webscraper
Though this didn't end up being utilized for the final project, the /scraper folder contains a web scraper designed
to extract course data from my.harvard and save it in a csv. To run the program, you will first need to follow the
selenium webdriver installation instructions at https://selenium.dev/. Feel free to set the USERNAME and PASSWORD
equal to your my.harvard login information. The program will open a new web browser, login, and wait for to to manually
complete Duo Authentication. Afterward, just sit back and wait as the program retrieves course data.

# Importing new course data
All course data is based on the courses.json in the /import folder. To replace the database with updated courses,
you just need to replace courses.json with a new file and rerun import_all.py. The first half of the script updates
the course database, and the second half updates the concentration requirements, so you can comment out parts as
needed.

New data is imported to the _test database. To quickly check the effects of the new import, you can change the
database used by application.py to the test database. Once satisfied, delete "yourharvard.db", rename the test
database as "yourharvard.db" and create a clone called "yourharvard_test.db" for future changes.

# Importing new concentration requirements
This relies on the concentrations.csv file in the /import folder. Exact syntax for course entries can be found
in the DESIGN document. Update the csv file and run import_all.py to save the new changes to the test database.
To quickly view the impacts of the change or change the test database to the real database, the same rules as
above apply.

# Running the website
Enter the yourHarvard containing this project, and execute "flask run" to run application.py.

# Register and Login:
You should be able to register at the top right! Make sure that your passwords match.
To log in, used the same username/password combo that you registered with.

# Course Explorer:
Here, you can explore the courses that count for a particular concentration. Simply choose a concentration you are
interested in, hit submit, and the courses that count for that concentration will appear! You can click the "Cou
rse Website" link to go to the course page or click the "Details" drop down to get a short course description. At
the top of the page (or in the page title), you can see which concentration is currently selected and how many
courses count (not including electives). To choose another concentration, click the dropdown and submit your new
choice.

# Schedule:
Here, you can plan out when to take the courses for your concentration!
Select your concentration, and all courses required for that concentration will appear as cards. Each block can be
dragged and dropped, so you can place them into the handy four-year table on the right! Note that for some
requirements, multiple courses can be used to satisfy the same requirement. To customize this, you can edit the
card text and type in which course you want to take. Note that you can also shuffle blocks around the schedule
table.

Once you finish, be sure to take a screenshot of your newly-organized four-year plan!
Thanks for using your.harvard!
