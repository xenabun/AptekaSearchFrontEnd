from flask import Flask, request, redirect, url_for, render_template
from flask_wtf import CSRFProtect, FlaskForm
from wtforms import StringField, SelectField, FloatField, BooleanField, HiddenField, SubmitField
import requests

app = Flask(__name__)
app.secret_key = 'aboba'
csrf = CSRFProtect(app)

shops = {'magnit': 'Магнит', 'rigla': 'Ригла', 'aptekaru': 'Аптека Ру'}
categories = {'dermacosmetika': 'Дермакосметика', 'dlapishevoreniya': 'Для пищеварения', 'vitaminiibad': 'Витамины и БАД'}
api_url = "https://maude-wardless-reba.ngrok-free.dev/api/"

class SearchForm(FlaskForm):
	page = HiddenField('Страница', default=1)
	min_page = HiddenField('Первая Страница', default=1)
	max_page = HiddenField('Последняя Страница', default=1)
	min_price_const = HiddenField('Минимальная цена', default=0)
	max_price_const = HiddenField('Максимальная цена', default=0)

	shop = SelectField('Магазин', choices=[
		('all', 'Все'),
		('magnit', 'Магнит'),
		('rigla', 'Ригла'),
		('aptekaru', 'Аптека Ру')
	])
	category = SelectField('Категория', choices=[
		('all', 'Все'),
		('dermacosmetika', 'Дермакосметика'),
		('dlapishevoreniya', 'Для пищеварения'),
		('vitaminiibad', 'Витамины и БАД')
	])
	min_price = FloatField('Минимальная цена')
	max_price = FloatField('Максимальная цена')
	discount = BooleanField('Со скидкой')
	name = StringField('Поиск')
	sort_by = SelectField('Сортировать', choices=[
		('id', 'Номер'),
		('price', 'Цену'),
		('name', 'Название'),
		('shop', 'Магазин'),
		('category', 'Категорию')
	])
	sort_dir = SelectField('По', choices=[
		('asc', 'Возрастанию'),
		('desc', 'Убыванию')
	])
	mysubmit = SubmitField('Найти')

@app.route('/')
def index():
	return redirect(url_for('search_page'))

@app.route("/search_page", methods=['GET', 'POST'])
def search_page():
	price_range = [0, 0]
	items = None
	items_amount = 0
	items_show_limit = 10
	page = 1
	min_page = 1
	max_page = 1
	exception = None

	form = SearchForm()

	try:
		request_url = api_url + 'price_range'
		response = requests.get(request_url)
		data = response.json()
		price_range = [data['min_price'], data['max_price']]
		
		form.min_price.data = data['min_price']
		form.min_price_const.data = data['min_price']
		form.max_price.data = data['max_price']
		form.max_price_const.data = data['max_price']
	except Exception as e:
		exception = str(e)

	if request.method == "POST":
		if request.form.get('page'):
			page = int(request.form.get('page'))
			form.page.data = int(request.form.get('page'))
		if request.form.get('shop'):
			form.shop.data = request.form.get('shop')
		if request.form.get('category'):
			form.category.data = request.form.get('category')
		if request.form.get('min_price'):
			form.min_price.data = float(request.form.get('min_price'))
		if request.form.get('max_price'):
			form.max_price.data = float(request.form.get('max_price'))
		if request.form.get('discount'):
			form.discount.data = True
		if request.form.get('name'):
			form.name.data = request.form.get('name')

		try:
			request_url = api_url + 'data?'
			queries = []

			if form.shop.data != 'all':
				queries.append(f'shop={shops[form.shop.data]}')
			if form.category.data != 'all':
				queries.append(f'category={categories[form.category.data]}')
			if len(form.name.data) > 0:
				queries.append(f'name={form.name.data}')
			if form.discount.data == True:
				queries.append(f'discount=true')
			queries.append(f'min_price={form.min_price.data}')
			queries.append(f'max_price={form.max_price.data}')
			queries.append(f'sort_by={form.sort_by.data}')
			queries.append(f'sort_dir={form.sort_dir.data}')
			queries.append(f'l={items_show_limit}')
			queries.append(f'page={page}')

			response = requests.get(request_url + '&'.join(queries))
			data = response.json()

			items = data['items']
			items_amount = data['items_amount']
			max_page = data['max_pages']

			form.max_page.data = max_page
		except Exception as e:
			exception = str(e)

	return render_template('index.html',
						form=form,
						exception=exception,
						items=items,
						items_amount=items_amount,
						items_show_limit=items_show_limit,
						price_range=price_range,
						page=page,
						min_page=min_page,
						max_page=max_page,
						shown_pages=[p for p in range(page - 1, page + 2) if p >= min_page and p <= max_page])
