import apteka_core as scrapper
import requests
from bs4 import BeautifulSoup
import re
import csv

## APTEKARU

file_name = '../data/aptekaru.csv'
shop = 'Аптека Ру'
url = 'https://apteka.ru'
APTEKARU_page_url = '?page={}'
APTEKARU_categories = {
	'Дермакосметика': '/category/derma_cosmetics',
	'Для пищеварения': '/category/diet',
	'Витамины и БАД': '/category/vitamin-mineral',
}

scrapper.clear_file(file_name)

def APTEKARU_get_max_pagination(page_name):
	response = requests.get(url + page_name, headers=scrapper.headers)
	soup = BeautifulSoup(response.content, "html.parser")

	pagination = soup.select_one('div[class="Paginator-wrapper"]')

	last_page_button = pagination.select_one('div:nth-last-child(1)')
	last_page_text = last_page_button.find('a')['href']
	last_page = int(''.join(re.findall(r'\d+\.?\d*', last_page_text)))

	return last_page

def APTEKARU_scrape_product_info(product, category):
	name_tag = product.select_one('span[class*="catalog-card__name"]')
	price_tag_container = product.select_one('div[class="card-price__summary"]')
	if not price_tag_container: return None
	price_tag = price_tag_container.select_one('span[class="moneyprice__content"]')
	price_tag_roubles = price_tag.select_one('span[class="moneyprice__roubles"]')
	price_tag_pennies = price_tag.select_one('span[class="moneyprice__pennies"]')
	old_price_tag_container = product.select_one('div[class="card-price__nodisc"]')
	old_price_tag = old_price_tag_container and old_price_tag_container.find('s')
	link_tag = product.select_one('a[class="catalog-card__photos"]')
	image_tag_container = product.select_one('picture[class*="CardMediasList__media"]')
	image_tag = image_tag_container and image_tag_container.find('img', src=True)

	name = name_tag.text.strip()
	price_text = price_tag_pennies != None and price_tag_roubles.text + price_tag_pennies.text or price_tag_roubles.text
	price = float(''.join(re.findall(r'\d+\.?\d*', price_text)))
	old_price = old_price_tag != None and float(''.join(re.findall(r'\d+\.?\d*', old_price_tag.text))) or price
	link = url + link_tag['href']
	image_url = image_tag and image_tag['src']

	data = [shop, category, name, price, old_price, link, image_url]

	return data

def APTEKARU_scrape():
	i = 1
	for category, category_url in APTEKARU_categories.items():
		max_page = APTEKARU_get_max_pagination(category_url)

		for cur_page in range(1, max_page + 1):
			soup = scrapper.get_dynamic_soup(
				url + category_url + APTEKARU_page_url.format(cur_page),
				'img[loading="eager"]'#picture[class*="CardMediasList__media"] > 
			)
			product_list = soup.select('div[class="CardsGrid"] > div')

			for product in product_list:
				print(f"{shop}-{category} [{cur_page}/{max_page}]: #{i}")
				i += 1
				data = APTEKARU_scrape_product_info(product, category)
				if data == None: continue

				with open(file_name, 'a', encoding='utf-8', newline='') as file:
					writer = csv.writer(file)
					writer.writerow(data)

APTEKARU_scrape()
