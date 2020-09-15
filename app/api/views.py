import re
from sqlalchemy import func, desc
from flask import Flask, request, jsonify, Blueprint, current_app
from app.models import Products, Reviews, Ratings 
from app.utils import add_review_to_db

api = Blueprint('api',__name__, url_prefix="/api")

@api.route('/product_rating')
def all_product_rating():
	"""
	Function returning the Rating string for all the products and product names using API call.
	"""
	prods = Products.query.all()
	res = [{"public_key" :prod.public_key , 
		"name":prod.name, 
		"rating_score": prod.rating[0].rating_string,
		"reviews" : [{"review" :review.review_string, "rating": review.rating} for review in prod.review]} for prod in prods]
	return jsonify(res), 200

@api.route('/product_rating/<public_key>')
def single_product_rating(public_key):
	"""
	Function returning the Rating string for all the products and product names using API call.
	"""
	prod = Products.query.filter(Products.public_key == public_key).first()
	res = {"public_key" :prod.public_key , 
		"name":prod.name, 
		"rating_score": prod.rating[0].rating_string,
		"reviews" : [{"review" :review.review_string, "rating": review.rating} for review in prod.review]} 
	return jsonify(res), 200


@api.route('/add_review', methods=['POST'])
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
			current_app.logger.info(f"Request received to add review for product {prod_public_key}...")
			message, is_new_rating = add_review_to_db(prod_public_key, review_string, rating)
			result = {'message':message, 'product_id': prod_public_key, 'review_evaluated': is_new_rating}
			return result, 201 if is_new_rating else 200
		else:
			raise ValueError("Invalid input. Product does not exist.")
	except KeyError:
		return {'error' :'Invalid input. Please provide the Product public key, review and rating between 1-5.'}, 400
	except ValueError as e:
		return {'error': str(e)}, 400

@api.route('/all_products')
def get_products():
	"""
	Returns a list of all the products
	"""
	return jsonify(Products.get_all_products()), 200

@api.route('/product/<public_key>')
def product_rating(public_key):
	"""
	Returns a particular products details.
	"""
	prod = Products.query.filter(Products.public_key == public_key).first()
	review_rating = Reviews.query.with_entities(func.count(Reviews.id), Reviews.rating).\
			filter(Reviews.product_id == prod.id).\
			group_by(Reviews.rating).all()

	review_rating = [{'rating': rev[1], 'rating_count': rev[0]} for rev in review_rating]
	return jsonify({
		'product_name': prod.name, 
		'public_key': prod.public_key, 
		'rating_string' :prod.rating[0].rating_string , 
		'reviews_ratings':review_rating}), 200
	