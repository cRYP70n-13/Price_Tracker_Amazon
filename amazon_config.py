from selenium import webdriver

DIRECTORY = 'reports'
NAME = 'PS4'
CURRENCY = '€'
MIN_PRICE = '275'
MAX_PRICE = '650'
FILTERS = {
	'min': MIN_PRICE,
	'max': MAX_PRICE
}
BASE_URL = "http://www.amazon.de/"


def get_chrome_web_driver(options):
	return webdriver.Chrome("./chromedriver", chrome_options=options)
