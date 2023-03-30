# Blue Alliance Web Scraper to Google Sheets
This Python script scrapes the Blue Alliance website for information about a robotics competition and writes the data to a Google Sheet. It uses the `pandas`, `gspread`, `gspread_dataframe`, `os`, `pydrive`, `python-dotenv`, `bs4,` and `selenium` packages to accomplish this.

## Prerequisites
To use this script, you'll need the following:
 - A Google account with access to Google Sheets
 - A The Blue Alliance event in which you are trying to analyze (specifically a link to the insights page of the event)
 - A local installation of Chrome, and the ChromeDriver executable file that matches your Chrome version

## Setup
1. Clone this repository to your local machine.

	    git clone https://github.com/ShinyShips/tba-webscraper.git
	    
2. Navigate to the project directory

3. Install the required packages:

		pip install -r requirements.txt

4. Create a .env file with the following variables:

		GOOGLE_APPLICATION_CREDENTIALS_JSON_PATH=<path_to_service_account_json>

		GOOGLE_SHEET_URL=<url_of_google_sheet>

		GOOGLE_WORKSHEET_NAME=<name_of_worksheet>

		WEBDRIVER_PATH=<path_to_chromedriver_executable>

		TBA_INSIGHTS_LINK=<url_of_blue_alliance_website>

5. Run the script:

		python tbaWebscrape.py

## How it works

The script uses the selenium package to open a Chrome window and navigate to the Blue Alliance website for a specific competition. It then uses BeautifulSoup to scrape the page for information about the teams and their scores.

The script writes the scraped data to a Pandas dataframe, which is then written to a Google Sheet using the gspread package. You can then take data from the Google Sheet and then do your own analysis.

## Future Work/Expansion
This can be be improved or expanded upon in a bunch of ways. Need more data than just cubes and cones? Add a bit more selenium code to capture those metrics and then create additional dictionaries for the data and then append it to the rows dictionary.

Future work may include finding all relevant data for a team across multiple events or just the alst event they attended. As this cannot really be used in the early stages of an event before all the teams have played.

## Contributing

Contributions are welcome! If you have any issues or suggestions for improvement, please open an issue or pull request on this repository.