from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy 
from config import Config

db = SQLAlchemy()

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

REVIEW_THRESHOLD = 1
PRODUCT_THRESHOLD = 4

def review_evaluation(product_list=None):
	"""
	input : Products that have new reviews
	output : Evaluated ratings string 
	Evaluates all the new reviews
	"""
	prod_rating = {}
	search_list = [x for x in db['products'] if x['id'] in product_list] if product_list else db['products']
	for prod in search_list:
		print(prod['name'])
		print("Product reviews")
		reviews = [x for x in db['reviews'] if x['prod_id'] == prod['id']]
		print(reviews)
		total_review_count = len(reviews)
		review_rating = {}
		for i in range(6):
			review_rating[i] = 0
		for review in reviews:
			rating = review['rating'] 
			review_rating[rating] += 1
		result = ''
		print(review_rating)
		for r in review_rating:
			result += str(review_rating[r])
		print(result)
		print("-------")
		prod_rating[prod['id']] = prod
	# pass

def check_threshold():
	"""
	Function calculates the number of new reviews per product. If crosses threshold then sends for evaluation.
	"""
	app.logger.info('Checking if the threshold has been crossed....')
	new_reviews = {}
	for review in [new_reviews for new_reviews in db['reviews'] if new_reviews['status'] == 'new']:
		if review['prod_id'] in new_reviews:
			new_reviews[review['prod_id']] += 1
		else:
			new_reviews[review['prod_id']] = 1
	products_to_evaluate = []
	for key, value in new_reviews:
		if value>=REVIEW_THRESHOLD:
			products_to_evaluate.append(key)
	review_evaluation(products_to_evaluate)

	print(new_reviews)


@app.route('/')
def home():
	"""
	View displays all the products available
	"""
	return "Hello World"

@app.route('/add_review', methods=['POST'])
def add_review():
	data = request.json
	print(data)
	product_id = data['prod_id']
	review_string = data['review_string']
	rating = data['rating']
	review = Reviews(prod_id=product_id, review_string=review_string, rating=rating, status="NEW")
	db.session.add(review)
	db.session.commit()
	app.logger.info(f"Product ID - {product_id}, Rating {rating} and Review - {review_string}")
	check_threshold()
	return {'message':'Review added'}, 200

if __name__ == '__main__':
	app.run(debug=True)