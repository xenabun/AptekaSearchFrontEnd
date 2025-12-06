from flask import Flask, request, render_template
import pandas as pd
import requests

app = Flask(__name__)

data_path = "data/data.csv"
shops = {'magnit': 'Магнит', 'rigla': 'Ригла', 'aptekaru': 'Аптека Ру'}
categories = {'dermacosmetika': 'Дермакосметика', 'dlapishevoreniya': 'Для пищеварения', 'vitaminiibad': 'Витамины и БАД'}
api_url = "https://maude-wardless-reba.ngrok-free.dev/api/"

@app.route("/", methods=['GET', 'POST'])
def search_page():
	form_data = request.form
	price_range = [0, 0]
	items = None
	items_amount = 0
	items_show_limit = 100
	page = 1
	exception = None

	try:
		request_url = api_url + 'price_range'
		response = requests.get(request_url)
		data = response.json()
		price_range = [data['min_price'], data['max_price']]
	except Exception as e:
		exception = str(e)

	if len(form_data) > 0:
		print(form_data)

		try:
			request_url = api_url + 'data?'
			queries = []

			if form_data.get('shop') != 'all':
				queries.append(f'shop={shops[form_data.get('shop')]}')
			if form_data.get('category') != 'all':
				queries.append(f'category={categories[form_data.get('category')]}')
			if len(form_data.get('name')) > 0:
				queries.append(f'name={form_data.get('name')}')
			if form_data.get('discount') == 'on':
				queries.append(f'discount=true')
			queries.append(f'min_price={form_data.get('min_price')}')
			queries.append(f'max_price={form_data.get('max_price')}')
			queries.append(f'page={page}')

			response = requests.get(request_url + '&'.join(queries))
			items = response.json()
			items_amount = len(items)
		except Exception as e:
			exception = str(e)

	return render_template('index.html',
						exception=exception,
						items=items,
						items_amount=items_amount,
						items_show_limit=items_show_limit,
						price_range=price_range)
