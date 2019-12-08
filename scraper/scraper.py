import csv
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

USERNAME = input("Username:")
PASSWORD = input("Password:")
num_pages = 363

# Launch Chrome
driver = webdriver.Chrome()
driver.get("https://www.pin1.harvard.edu/cas/login?service=https%3a%2f%2fportal.my.harvard.edu%2f")

# Log In
element = driver.find_element_by_name("username")
element.send_keys(USERNAME)
element = driver.find_element_by_name("password")
element.send_keys(PASSWORD)
element = driver.find_element_by_name("source")
element.send_keys("HARVARDKEY")
driver.find_element_by_name("submit").click()
time.sleep(5)
# Wait for Duo Authentication
while "Duo" in driver.title:
	time.sleep(1)

# Scrape site data
"""This is where you enter how many pages there are"""
for page in range(num_pages):
	# Access course page
	URL = "https://portal.my.harvard.edu/psp/hrvihprd/EMPLOYEE/EMPL/h/?tab=HU_CLASS_SEARCH&SearchReqJSON=%7B%22ExcludeBracketed%22%3Atrue%2C%22SaveRecent%22%3Atrue%2C%22Facets%22%3A%5B%5D%2C%22PageNumber%22%3A" + str(page + 1) + "%2C%22SortOrder%22%3A%5B%22IS_SCL_SUBJ_CAT%22%5D%2C%22TopN%22%3A%22%22%2C%22PageSize%22%3A%22%22%2C%22SearchText%22%3A%22*%22%7D"
	driver.get(URL)
	# Store relevant data
	names = driver.find_elements_by_class_name("isSCL_RBC")
	# Verify new page is loaded
	while not names:
		time.sleep(1)
		names = driver.find_elements_by_class_name("isSCL_RBC")
	# Continue collecting data
	codes = driver.find_elements_by_class_name("isSCL_RBSCN")
	instructors = driver.find_elements_by_class_name("isSCL_RBI")
	schools = driver.find_elements_by_class_name("isSCL_RBDP")
	departments = driver.find_elements_by_class_name("isSCL_RBS")
	terms = driver.find_elements_by_class_name("isSCL_RBT")
	sessions = driver.find_elements_by_class_name("isSCL_Session")
	##days = driver.find_elements_by_xpath("//div/div[@class='isSCL_RBM']")
	times = driver.find_elements_by_class_name("isSCL_RBSET")
	descriptions = driver.find_elements_by_class_name("isSCL_RBD")
	# Write to file
	with open('output.csv','a+', newline='', encoding="utf-8") as result_file:
		for i in range(len(names)):
			RESULTS = [names[i].text,codes[i].text,instructors[i].text,schools[i].text,departments[i].text,terms[i].text,sessions[i].text,times[i].text,descriptions[i].text]
			wr = csv.writer(result_file, delimiter=',').writerow(RESULTS)
# End session
driver.quit()