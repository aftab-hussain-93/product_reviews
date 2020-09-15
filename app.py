import re
from flask import Flask, request, render_template, redirect, url_for, jsonify
from config import Config
from extensions import db
from models import Reviews, Products, Ratings
from forms import ReviewField
from utils import add_review_to_db, update_rating_score, review_evaluation, check_threshold


def register_extensions(app):
    db.init_app(app)
    return

def create_app(config_object):
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config_object)
    register_extensions(app)
    return app

app = create_app(Config)

@app.route('/home')
@app.route('/')
def home():
	"""
	Home page - Displays all the Products available for review.
	"""
	form = ReviewField()
	products = Products.query.all()
	return render_template('home.html', form=form, products=products)

@app.route('/submit_review', methods=['POST'])
def add_review():
	"""
	View to add review to the Database from the application front end using AJAX.
	"""
	form = ReviewField()
	if form.validate_on_submit():
		prod_public_key = request.json['prod_id']
		review_string = form.review.data
		rating = form.rating.data
		message, is_new_rating = add_review_to_db(prod_public_key, review_string, rating)
		return {'message': message }, 200
	return jsonify({'error' : form.errors if form.errors else 'Bad Request'}), 400

@app.route('/api/product_rating')
def all_product_rating():
	"""
	Function returning the Rating string for all the products and product names using API call.
	"""
	prods = Products.query.all()
	res = [{prod.id : {prod.name : prod.rating[0].rating_string}} for prod in prods]
	return jsonify(res), 200


@app.route('/api/add_review', methods=['POST'])
def api_add_review():
	"""
	View function to add review through an API call.
	"""
	data = request.json
	try:
		prod_public_key = data['product_id']
		review_string = str(data['review_string'])
		rating = int(data['rating'])
		if rating < 1 or rating > 5:
			raise ValueError("Invalid input. Rating should be between 1-5")
		product = Products.query.filter(Products.public_key == prod_public_key).first()
		if product:
			app.logger.info(f"Request received to add review for product {prod_public_key}...")
			message, is_new_rating = add_review_to_db(prod_public_key, review_string, rating)
			result = {'message':message, 'product_id': prod_public_key, 'review_evaluated': is_new_rating}
			return result, 201 if is_new_rating else 200
		else:
			raise ValueError("Invalid input. Product does not exist.")
	except KeyError:
		return {'error' :'Invalid input. Please provide the Product public key, review and rating between 1-5.'}, 400
	except ValueError as e:
		return {'error': str(e)}, 400

@app.route('/api/all_products')
def get_products():
	"""
	Returns a list of all the products
	"""
	return Products.get_all_products()

@app.route('/api/product/<public_key>')
def product_rating(public_key):
	"""
	Returns a particular products details.
	"""
	prod = Products.query.filter(Products.public_key == public_key).first()
	rt_string = prod.rating.rating_string
	return {'name' : prod.name, 'public_key': prod.public_key, 'rating_string': rt_string}


@app.template_filter()
def rating_list(rating_string):
	"""
	Jinja filter to parse the rating string to display details
	"""
	rating_values = re.findall(r'\d+', rating_string)
	return rating_values

if __name__ == '__main__':
	app.run(debug=True)




