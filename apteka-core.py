import requests
from bs4 import BeautifulSoup
import re
import csv
from playwright.sync_api import sync_playwright, expect

headers = {
	'User-Agent':
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
}
file_name = 'aptekaru-data.csv'
def clear_file():
	with open(file_name, 'w', encoding='utf-8', newline='') as file:
		writer = csv.writer(file)
		writer.writerow(['Магазин', 'Категория', 'Название', 'Цена', 'Цена без скидки', 'Ссылка', 'Изображение'])
def get_dynamic_soup(url: str, selector: str|None = None) -> BeautifulSoup:
	with sync_playwright() as p:
		browser = p.chromium.launch()#headless=False)
		page = browser.new_page()
		page.goto(url, wait_until="domcontentloaded")

		if selector:
			page.evaluate("""() => {
				document.querySelectorAll('img[loading="lazy"]').forEach((img) => {
					//const image = img;// as HTMLImageElement;
					img.setAttribute('loading', 'eager'); // Force eager loading
					//const source = image.src;
					//image.src = '';  // Reset src to reload the image
					//image.src = source; // Set src back to original
				})
			}""")

			try:
				lazy_images = page.locator(selector)
				for lazy_image in lazy_images.all():
					lazy_image.scroll_into_view_if_needed()
					expect(lazy_image).to_have_js_property('complete', True)
					expect(lazy_image).not_to_have_js_property('naturalWidth', 0)

				page.wait_for_selector(selector)
			except:
				pass

		soup = BeautifulSoup(page.content(), "html.parser")
		browser.close()
		return soup

# clear_file()

## MAGNIT

shop = 'Магнит'
url = 'https://apteka.magnit.ru'
MAGNIT_page_url = '?page={}'
MAGNIT_categories = {
	'Дермакосметика': '/catalog/ukhod/dermacosmetika',
	'Для пищеварения': '/catalog/lekarstva/zheludok_kishechnik_pechen',
	'Витамины и БАД': '/catalog/vitaminy_i_bad',
}

def MAGNIT_get_max_pagination(page_name):
	response = requests.get(url + page_name, headers=headers)
	soup = BeautifulSoup(response.content, "html.parser")
	
	pagination = soup.select_one('nav[class="catalog-pagination"]')
	
	last_page_button = pagination.find('div').select_one('a:nth-last-child(2)')
	last_page_span = last_page_button.select_one('span[class="pl-button__title"]')
	last_page_text = last_page_span.text
	last_page = int(last_page_text)
	
	return last_page

def MAGNIT_scrape_product_info(product, category):
	name_tag = product.select_one('p[class*="product-card__title"]')
	price_tag = product.select_one('span[class*="product-price__current"]')
	old_price_tag = product.select_one('span[class*="product-price__previous"]')
	link_tag = product.find('a', href=True)
	image_tag_container = product.select_one('div[class="product-card__img"]')
	image_tag = image_tag_container.find('img', src=True)

	name = name_tag.text.strip()
	price = float(''.join(re.findall(r'\d+\.?\d*', price_tag.text)))
	old_price = old_price_tag != None and float(''.join(re.findall(r'\d+\.?\d*', old_price_tag.text))) or price
	link = url + link_tag['href']
	image_url = image_tag['src']

	data = [shop, category, name, price, old_price, link, image_url]

	return data

def MAGNIT_scrape():
	i = 1
	for category, category_url in MAGNIT_categories.items():
		max_page = MAGNIT_get_max_pagination(category_url)

		for cur_page in range(1, max_page + 1):
			soup = get_dynamic_soup(
				url + category_url + MAGNIT_page_url.format(cur_page),
				'img[loading="eager"][class="custom-image__image"]'
			)
			prod_list_container = soup.select_one('ul[class="product-list"]')
			product_list = prod_list_container and prod_list_container.find_all('li')
			if not product_list: continue

			for product in product_list:
				print(f"{shop}-{category} [{cur_page}/{max_page}]: #{i}")
				i += 1
				data = MAGNIT_scrape_product_info(product, category)

				with open(file_name, 'a', encoding='utf-8', newline='') as file:
					writer = csv.writer(file)
					writer.writerow(data)

# MAGNIT_scrape()

## RIGLA

shop = 'Ригла'
url = 'https://www.rigla.ru'
RIGLA_page_url = '?p={}'
RIGLA_categories = {
	'Дермакосметика': '/cat/lekarstvennye-preparaty/kozha-dermatologicheskie-preparaty',
	'Для пищеварения': '/cat/lekarstvennye-preparaty/pishchevaritelnaya-sistema',
	'Витамины и БАД': '/cat/vitaminy-i-bady',
}

def RIGLA_get_max_pagination(page_name):
	response = requests.get(url + page_name, headers=headers)
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
			soup = get_dynamic_soup(
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

# RIGLA_scrape()

## APTEKARU

shop = 'Аптека Ру'
url = 'https://apteka.ru'
APTEKARU_page_url = '?page={}'
APTEKARU_categories = {
	'Дермакосметика': '/category/derma_cosmetics',
	'Для пищеварения': '/category/diet',
	'Витамины и БАД': '/category/vitamin-mineral',
}

def APTEKARU_get_max_pagination(page_name):
	response = requests.get(url + page_name, headers=headers)
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
			soup = get_dynamic_soup(
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

# APTEKARU_scrape()
