from flask import Flask, request
from sqlalchemy import func
from config import Config
from extensions import db
from models import Reviews, Products, Ratings


def register_extensions(app):
    db.init_app(app)
    return

def create_app(config_object):
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config_object)
    register_extensions(app)
    return app

app = create_app(Config)


REVIEW_THRESHOLD = 1
PRODUCT_THRESHOLD = 4


def update_db(prod_rating):
	for prod_id, rating in prod_rating.items():
		print(f"Product ID {prod_id} - {rating}")
		count = Ratings.query.filter(Ratings.product_id==prod_id).count()
		print(count)
		if count > 0:
			# Updating
			print(f"Updating to rating {rating}")
			rating = Ratings.query.filter(Ratings.product_id == prod_id).first()
			rating.rating_string = str(rating)
			print("Updating")
		else:
			# Inserting
			rating = Ratings(product_id=prod_id, rating_string=str(rating))
			db.session.add(rating)
			print("Inserting")
	db.session.commit()

def review_evaluation(product_list=None):
	"""
	input : Products that have new reviews
	output : Evaluated ratings string and updates the database
	Evaluates all the new reviews
	"""
	products  = Products.query.filter(Products.id.in_(product_list)) if product_list else Products.query
	products = products.all()
	prod_rating = {}
	for product in products:
		review_rating = {}
		for i in range(6):
			review_rating[i] = 0

		rating_string = ''
		
		for review in product.review:
			if review.status == 'PROCESSED':
				review_rating[review.rating] += 1

		for key, val in sorted(review_rating.items()):
			print("The rating value - {}".format(key))
			rating_string += str(val)
		print(f"The overall rating score for product {product.id} is {rating_string}")
		prod_rating[product.id] = rating_string
	return prod_rating

def check_threshold():
	"""
	Function calculates the number of new reviews per product. If crosses threshold then sends for evaluation.
	"""
	app.logger.info('Checking if the threshold has been crossed....')

	# Getting all the products with the count of new reviews

	prod_review = Products.query.with_entities(Products.id,func.count(Products.id)).\
		join(Reviews).\
		filter(Reviews.product_id == Products.id, Reviews.status=='NEW').\
		group_by(Products.id).\
		having(func.count(Products.id) > REVIEW_THRESHOLD)

	prod_count = prod_review.count()
	print("The product count is {}".format(prod_count))	

	if prod_count > PRODUCT_THRESHOLD:
		review_count = prod_review.all()
		# Send for evaluation
		prod_ids = [p[0] for p in review_count]
		new_reviews = Reviews.query.filter(Reviews.status == 'NEW', Reviews.product_id.in_(prod_ids)).all()
		for review in new_reviews:
			review.status = 'PROCESSED'
		db.session.commit()
		prod_overall_rating = review_evaluation(prod_ids)
		update_db(prod_overall_rating)
		return True
	app.logger.info('Threshold for evaluation has not been reached')
	return False


@app.route('/test')
def test():
	prod_overall_rating = review_evaluation()
	update_db(prod_overall_rating)
	return "testing"

@app.route('/api/productrating')
def get_product_rating():
	prod_overall_rating = review_evaluation()
	return prod_overall_rating, 200

@app.route('/')
def home():
	"""
	View displays all the products available
	"""
	return "Hello World"

@app.route('/add_review', methods=['POST'])
def add_review():
	data = request.json
	product_id = data['prod_id']
	review_string = data['review_string']
	rating = data['rating']
	review = Reviews(product_id=product_id, review_string=review_string, rating=rating)
	db.session.add(review)
	db.session.commit()
	app.logger.info(f"Product ID - {product_id}, Rating {rating} and Review - {review_string}")
	result = check_threshold()
	message = 'Review added. ' + ('New rating score evaluated.' if result else 'Rating score not evaluated.')
	app.logger.info(message)
	return {'message':message}, 200

if __name__ == '__main__':
	app.run(debug=True)




