# Importing necessary libraries
import pandas as pd
import gspread
import os
import statbotics
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from dotenv import load_dotenv

# Loading the .env file
load_dotenv()

# Initializing constants from the .env file
GOOGLE_APPLICATION_CREDENTIALS_JSON_PATH=os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON_PATH')
GOOGLE_SHEET_URL=os.getenv('GOOGLE_SHEET_URL')
GOOGLE_WORKSHEET_NAME=os.getenv('GOOGLE_WORKSHEET_NAME')
WEBDRIVER_PATH=os.getenv('WEBDRIVER_PATH')
EVENT_ID=os.getenv('EVENT_ID')

# Defining the Google Sheets and Drive API credentials
scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
creds = Credentials.from_service_account_file(
    GOOGLE_APPLICATION_CREDENTIALS_JSON_PATH, 
    scopes=scopes
)

# Initializing the Statbotics API interface
sb = statbotics.Statbotics()

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
driver.get(f'https://www.thebluealliance.com/event/{EVENT_ID}#event-insights')

# Selecting the desired elements on the webpage using Selenium
insights = driver.find_element(By.CLASS_NAME, 'btn-group')
cones = driver.find_element(By.ID, 'dropdown_Total_Cones_Scored')
cubes = driver.find_element(By.ID, 'dropdown_Total_Cubes_Scored')

# Scraping the HTML content of the page using BeautifulSoup for OPR data
page_source = driver.page_source
opr_soup = BeautifulSoup(page_source, 'html.parser')
opr_rows = opr_soup.select('#coprTableBody tr')

# Simulating a mouse click on the desired elements using Selenium
insights.click()
cones.click()

# Scraping the HTML content of the page using BeautifulSoup for cone data
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')
table_rows = soup.select('#coprTableBody tr')

# Simulating another mouse click on the desired elements using Selenium
insights.click()
cubes.click()

# Scraping the HTML content of the page for the cubes data using BeautifulSoup for cube data
cubes_source = driver.page_source
cube_soup = BeautifulSoup(cubes_source, 'html.parser')
cube_rows = cube_soup.select('#coprTableBody tr')

# Creating a dictionary to store the OPR data for each team
opr_dict = {}
for row in opr_rows:
    team_number = row.find('td').find_next_sibling('td').text
    opr = row.find_all('td')[2].text
    opr_dict[team_number] = opr

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
    opr = opr_dict.get(team_number, '')
    stats = sb.get_team_event(int(team_number),EVENT_ID,['epa_end', 'auto_epa_end', 'teleop_epa_end', 'endgame_epa_end'])
    rows.append({
        'teamNumber': team_number,
        'cones': cones,
        'cubes': cubes,
        'opr': opr,
        'epa': stats['epa_end'],
        'autoEpa': stats['auto_epa_end'],
        'teleopEpa': stats['teleop_epa_end'],
        'endgameEpa': stats['endgame_epa_end'],

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