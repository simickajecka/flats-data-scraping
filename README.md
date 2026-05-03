Clone this project: git clone https://github.com/simickajecka/flats-data-scraping.git name_dir
Navigate to your new directory: cd name_dir
Create a Python Virtual Environment: python -m venv name_env
Activate the Python Virtual Environment:
(Windows) env\Scripts\activate
(macOS/Linux) source env/bin/activateenv/Scripts/activate
Install dependencies: pip install -r requirements.txt
Check: scrapy list
cd flatsscraper/flatsscraper/spiders
Running the scrapy project (run spider): scrapy crawl flatspider
