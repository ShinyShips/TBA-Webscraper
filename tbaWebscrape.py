# Importing necessary libraries
import pandas as pd
import gspread
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from dotenv import load_dotenv

load_dotenv()

GOOGLE_APPLICATION_CREDENTIALS_JSON_PATH=os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON_PATH')
GOOGLE_SHEET_URL=os.getenv('GOOGLE_SHEET_URL')
GOOGLE_WORKSHEET_NAME=os.getenv('GOOGLE_WORKSHEET_NAME')
WEBDRIVER_PATH=os.getenv('WEBDRIVER_PATH')
TBA_INSIGHTS_LINK=os.getenv('TBA_INSIGHTS_LINK')

# Defining the Google Sheets and Drive API credentials
scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
creds = Credentials.from_service_account_file(
    GOOGLE_APPLICATION_CREDENTIALS_JSON_PATH, 
    scopes=scopes
)

# Authorizing the Google Sheets API
gc = gspread.authorize(creds)

# Authorizing the Google Drive API
gauth = GoogleAuth()
drive = GoogleDrive(gauth)

# Opening the Google Sheet by URL
gs = gc.open_by_url(GOOGLE_SHEET_URL)

# Selecting the worksheet to be used
worksheet1 = gs.worksheet(GOOGLE_WORKSHEET_NAME)

# Initializing the Chrome driver and opening the desired webpage
driver = webdriver.Chrome(WEBDRIVER_PATH)
driver.get(TBA_INSIGHTS_LINK)

# Selecting the desired elements on the webpage using Selenium
insights = driver.find_element(By.CLASS_NAME, 'btn-group')
cones = driver.find_element(By.ID, 'dropdown_Total_Cones_Scored')
cubes = driver.find_element(By.ID, 'dropdown_Total_Cubes_Scored')

# Simulating a mouse click on the desired elements using Selenium
insights.click()
cones.click()

# Scraping the HTML content of the page using BeautifulSoup
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')
table_rows = soup.select('#coprTableBody tr')

# Simulating another mouse click on the desired elements using Selenium
insights.click()
cubes.click()

# Scraping the HTML content of the page for the cubes data using BeautifulSoup
cubes_source = driver.page_source
cube_soup = BeautifulSoup(cubes_source, 'html.parser')
cube_rows = cube_soup.select('#coprTableBody tr')

# Creating a dictionary to store the cubes data for each team
cubes_dict = {}
for row in cube_rows:
    team_number = row.find('td').find_next_sibling('td').text
    cubes = row.find_all('td')[2].text
    cubes_dict[team_number] = cubes

# Creating a list of dictionaries to store the data for each team
rows = []
for row in table_rows:
    team_number = row.find('td').find_next_sibling('td').text
    cones = row.find_all('td')[2].text
    cubes = cubes_dict.get(team_number, '')
    rows.append({
        'teamNumber': team_number,
        'cones': cones,
        'cubes': cubes,
    })

# Creating a Pandas DataFrame from the list of dictionaries
output = pd.DataFrame(rows)

# Clearing the worksheet and writing the DataFrame to the worksheet
worksheet1.clear()
set_with_dataframe(
    worksheet=worksheet1, 
    dataframe=output, 
    include_index=False,
    include_column_header=True, 
    resize=True
)

# Printing the output DataFrame
print(output)