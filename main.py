import time
from selenium.webdriver.common.keys import Keys
from amazon_config import (
	get_web_driver_options,
	get_chrome_web_driver,
	set_ignore_certificate_error,
	set_browser_as_incognito,
	set_automation_as_head_less,
	NAME,
	CURRENCY,
	FILTERS,
	BASE_URL,
	DIRECTORY
)
from selenium.common.exceptions import NoSuchElementException
import json
from datetime import datetime
