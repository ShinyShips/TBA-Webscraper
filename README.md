# Blue Alliance Web Scraper to Google Sheets
This Python script scrapes the Blue Alliance website for information about a robotics competition, accesses data from the statbotics API and writes the data to a Google Sheet. It uses the `pandas`, `gspread`, `gspread_dataframe`, `os`, `pydrive`, `python-dotenv`, `bs4`, `statbotics`, and `selenium` packages to accomplish this.

## Prerequisites
To use this script, you'll need the following:
 - A Google account with access to Google Sheets
 - The event ID from TheBlueAlliance.com or Statbotics.io in which you are trying to analyze i.e. 2023paben
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

		EVENT_ID=<id_of_event>

		for example, the ID of the 2023 FMA District Bensalem event can be found at the end of this url after /event/ https://www.thebluealliance.com/event/2023paben . This is the same id used on Statbotics

5. Run the script:

		python tbaWebscrape.py

## How it works

The script uses the selenium package to open a Chrome window and navigate to the Blue Alliance website for a specific competition. It then uses BeautifulSoup to scrape the page for information about the team's OPR, number of cones, and number of cubes. It then calls the statbotics API for each team at the event and gathers the overall EPA, auto EPA, teleop EPA, and endgame EPA.

The script writes the scraped data to a Pandas dataframe, which is then written to a Google Sheet using the gspread package. You can then take data from the Google Sheet and then do your own analysis.

Currently, this is being used to gather information to be dumped into a database for use within an internal scouting app.

## Future Work/Expansion
This can be be improved or expanded upon in a bunch of ways. Need more data than what was provided? Add a bit more selenium code to capture those metrics and then create additional dictionaries for the data and then append it to the rows dictionary.

Future work may include finding all relevant data for a team across multiple events or just the all events they attended. As this cannot really be used in the early stages of an event before all the teams have played. Also possibly scraping the EPA breakdown from statbotics or just waiting until that is added to the API to add that info.

## Contributing

Contributions are welcome! If you have any issues or suggestions for improvement, please open an issue or pull request on this repository.