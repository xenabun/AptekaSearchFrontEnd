import apteka_core as scrapper
import requests
from bs4 import BeautifulSoup
import re
import csv

## RIGLA

file_name = '../data/rigla.csv'
shop = 'Ригла'
url = 'https://www.rigla.ru'
RIGLA_page_url = '?p={}'
RIGLA_categories = {
	'Дермакосметика': '/cat/lekarstvennye-preparaty/kozha-dermatologicheskie-preparaty',
	'Для пищеварения': '/cat/lekarstvennye-preparaty/pishchevaritelnaya-sistema',
	'Витамины и БАД': '/cat/vitaminy-i-bady',
}

scrapper.clear_file(file_name)

def RIGLA_get_max_pagination(page_name):
	response = requests.get(url + page_name, headers=scrapper.headers)
	soup = BeautifulSoup(response.content, "html.parser")

	pagination = soup.select_one('div[class="pagination"]')

	last_page_button = pagination.select_one('div:nth-last-child(2)')
	last_page_text = last_page_button.find('div').text
	last_page = int(last_page_text)
	
	return last_page

def RIGLA_scrape_product_info(product, category):
	name_tag = product.select_one('a[class="product__title"]')
	price_tag = product.select_one('span[class="product__active-price-number"]')
	meta = product.select_one('div[class="product__meta"]')
	old_price_container = meta.select_one('span[class*="product__underline-price"]')
	old_price_tag = old_price_container and old_price_container.select_one('span[class="currency__price"]')
	link_tag = name_tag
	image_tag_container = product.select_one('div[class="product-info__img-wrapper"]')
	image_tag = image_tag_container.find('meta', itemprop='image')

	name = name_tag.text.strip()
	price = float(''.join(re.findall(r'\d+\.?\d*', price_tag.text)))
	old_price = old_price_tag != None and float(''.join(re.findall(r'\d+\.?\d*', old_price_tag.text))) or price
	link = url + link_tag['href']
	image_url = image_tag['content']

	data = [shop, category, name, price, old_price, link, image_url]
	
	return data

def RIGLA_scrape():
	i = 1
	for category, category_url in RIGLA_categories.items():
		max_page = RIGLA_get_max_pagination(category_url)

		for cur_page in range(1, max_page + 1):
			soup = scrapper.get_dynamic_soup(
				url + category_url + RIGLA_page_url.format(cur_page)
			)
			product_list = soup.select_one('div[class="product-list-mode-grid"]').select('div[class*="product-list-mode-grid__item"]')

			for product in product_list:
				print(f"{shop}-{category} [{cur_page}/{max_page}]: #{i}")
				i += 1
				data = RIGLA_scrape_product_info(product, category)

				with open(file_name, 'a', encoding='utf-8', newline='') as file:
					writer = csv.writer(file)
					writer.writerow(data)

RIGLA_scrape()
