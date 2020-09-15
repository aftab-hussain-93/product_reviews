from flask import current_app as app
from sqlalchemy import func
from extensions import db
from models import Reviews, Products, Ratings

# Starting with 0, every new review triggers an evaluation
REVIEW_THRESHOLD = 0
PRODUCT_THRESHOLD = 0

def add_review_to_db(product_public_key, review_string, rating):
	"""
	Function to add the review to the database
	input  : product public key, review and rating
	"""
	with app.app_context():
		prod = Products.query.filter(Products.public_key == product_public_key).first()
		review = Reviews(product=prod, review_string=review_string, rating=rating)
		db.session.add(review)
		db.session.commit()
		app.logger.info(f"Review added to Database for product {prod.public_key}, review ID {review.id} ...")
		new_score_evaluated = check_threshold()
		message = 'Review added. ' + ('New rating score evaluated.' if new_score_evaluated else 'Rating score not evaluated.')
		app.logger.info(message)
		return message, new_score_evaluated

def check_threshold():
	"""
	Function calculates the number of new reviews per product. If crosses threshold then sends for evaluation.
	"""
	with app.app_context():
		app.logger.info('Checking if the new reviews have to evaluated...')
		app.logger.info(f'Existing product count threshold {PRODUCT_THRESHOLD} and review count threshold {REVIEW_THRESHOLD}')

		app.logger.info(f'Retrieving list of products with more than {REVIEW_THRESHOLD} new reviews...')
		prod_review = Products.query.with_entities(Products.id,func.count(Products.id)).\
			join(Reviews).\
			filter(Reviews.product_id == Products.id, Reviews.status=='NEW').\
			group_by(Products.id).\
			having(func.count(Products.id) > REVIEW_THRESHOLD)
		prod_count = prod_review.count()

		app.logger.info(f"Product count {prod_count}")

		if prod_count > PRODUCT_THRESHOLD:
			app.logger.info(f'Reviews are being evaluated')
			products_to_review = prod_review.all()
			# Send for evaluation
			prod_ids = [p[0] for p in products_to_review]
			new_reviews = Reviews.query.filter(Reviews.status == 'NEW', Reviews.product_id.in_(prod_ids)).all()
			for review in new_reviews:
				review.status = 'PROCESSED'
			db.session.commit()
			prod_overall_rating = review_evaluation(prod_ids)
			update_rating_score(prod_overall_rating)
			return True
		app.logger.info('Threshold for evaluation has not been reached')
		return False


def update_rating_score(prod_rating):
	"""
	Function to update the Rating Score for each product in the input dictionary.
	Input - Dict containing product public key and rating score string.
	"""
	for public_key, rating in prod_rating.items():
		with app.app_context():
			prod = Products.query.filter(Products.public_key == public_key).first()
			count = Ratings.query.filter(Ratings.product_id==prod.id).count()
			if count > 0:
				# Updating
				app.logger.info(f"Updating to rating score of prod {prod.name}")
				rt = Ratings.query.filter(Ratings.product_id == prod.id).first()
				rt.rating_score = rating
			else:
				# Inserting
				rt = Ratings(product_id=prod.id, rating_score=rating)
				db.session.add(rt)
				app.logger.info("Inserting new rating score")
			db.session.commit()

def review_evaluation(product_list):
	"""
	input : Products that have new reviews
	output : Evaluate the reviews and store the new rating string
	"""
	with app.app_context():
		products  = Products.query.filter(Products.id.in_(product_list))
		products = products.all()

		# Dictionary to store the newly evaluated rating string for each Product
		prod_rating = {}
		for product in products:
			review_rating = {}
			for i in range(1,6):
				review_rating[i] = 0

			rating_string = ''
			# Creating dictionary to store the count of review per rating
			for review in product.review:
				if review.status == 'PROCESSED':
					review_rating[review.rating] += 1
			rating_list = '*'.join([str(val) for key, val in sorted(review_rating.items())])
			prod_rating[product.public_key] = rating_list
		return prod_rating

