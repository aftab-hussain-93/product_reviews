import re
from flask import Flask, request, render_template, jsonify, Blueprint
from app.models import Reviews, Products, Ratings
from app.forms import ReviewField
from app.utils import add_review_to_db


main = Blueprint('main',__name__)

@main.route('/home')
@main.route('/')
def home():
	"""
	Home page - Displays all the Products available for review.
	"""
	page = request.args.get('page', 1, type=int)
	form = ReviewField()
	products = Products.query.paginate(page=page, per_page=5)
	return render_template('home.html', form=form, products=products)

@main.route('/submit_review', methods=['POST'])
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

@main.app_template_filter()
def rating_list(rating_string):
	"""
	Jinja filter to parse the rating string to display details
	"""
	rating_values = re.findall(r'\d+', rating_string)
	return rating_values