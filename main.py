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


class GenerateReport:
	def __init__(self, file_name, filters, base_link, currency, data):
		self.data = data
		self.file_name = file_name
		self.filters = filters
		self.base_link = base_link
		self.currency = currency
		report = {
			'title': self.file_name,
			'date': self.get_now(),
			'best_item': self.get_best_item(),
			'currency': self.currency,
			'filters': self.filters,
			'base_link': self.base_link,
			'products': self.data
		}
		print("Creating report...")
		with open(f'{DIRECTORY}/{file_name}.json', 'w') as f:
			json.dump(report, f)
		print("Done...")

	@staticmethod
	def get_now():
		now = datetime.now()
		return now.strftime("%d/%m/%Y %H:%M:%S")

	def get_best_item(self):
		try:
			return sorted(self.data, key=lambda k: k['price'])[0]
		except Exception as e:
			print(e)
			print("Problem with sorting items")
			return None


class AmazonAPI:
	def __init__(self, search_term, filters, base_url, currency):
		self.base_url = base_url
		self.search_term = search_term
		options = get_web_driver_options()
		# set_automation_as_head_less(options)
		set_ignore_certificate_error(options)
		set_browser_as_incognito(options)
		self.driver = get_chrome_web_driver(options)
		self.currency = currency
		self.price_filter = f"&rh=p_36%3A{filters['min']}00-{filters['max']}00"

	def run(self):
		print("Starting Script...")
		print(f"Looking for {self.search_term} products...")
		links = self.get_products_links()
		if not links:
			print("Stopped script.")
			return
		print(f"Got {len(links)} links to products...")
		print("Getting info about products...")
		products = self.get_products_info(links)
		print(f"Got info about {len(products)} products...")
		self.driver.quit()
		return products

	def get_products_links(self):
		self.driver.get(self.base_url)
		element = self.driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]')
		element.send_keys(self.search_term)
		element.send_keys(Keys.ENTER)
		time.sleep(2)  # wait to load page
		self.driver.get(f'{self.driver.current_url}{self.price_filter}')
		print(f"Our url: {self.driver.current_url}")
		time.sleep(2)  # wait to load page
		result_list = self.driver.find_elements_by_class_name('s-result-list')
		links = []
		try:
			results = result_list[0].find_elements_by_xpath(
				"//div/span/div/div/div[2]/div[2]/div/div[1]/div/div/div[1]/h2/a")
			links = [link.get_attribute('href') for link in results]
			return links
		except Exception as e:
			print("Didn't get any products...")
			print(e)
			return links

def get_products_info(self, links):
		asins = self.get_asins(links)
		products = []
		for asin in asins:
			product = self.get_single_product_info(asin)
			if product:
				products.append(product)
		return products

def get_asins(self, links):
		return [self.get_asin(link) for link in links]

def get_single_product_info(self, asin):
        print(f"Product ID: {asin} - getting data...")
        product_short_url = self.shorten_url(asin)
        self.driver.get(f'{product_short_url}?language=en_GB')
        time.sleep(2)
        title = self.get_title()
        seller = self.get_seller()
        price = self.get_price()
        if title and seller and price:
            product_info = {
                'asin': asin,
                'url': product_short_url,
                'title': title,
                'seller': seller,
                'price': price
            }
            return product_info
        return None
