import random, csv
from app import db, app
from models import Products, Reviews, Ratings

reviews_ratings = [('Really good',4), ('Excellent', 5), ('Average',3), ('Bad', 2), ('Horrible', 1), ('Dont Buy', 0) ]

# all_prods = []
# with open('testing/flipkart_data_sample.csv') as csv_file:
# 	csv_reader = csv.reader(csv_file, delimiter=',')
# 	for row in csv_reader:
# 		name = row[0]
# 		image = row[1]
# 		all_prods.append({'product_name':name, 'image':image})
with app.app_context():
	# Inital setup. Create DB and Add all products.
	# db.create_all()
	# for prod in all_prods:
	# 	p = Products(name = prod['product_name'], image_url = prod['image'] )
	# 	db.session.add(p)
# print("All products added")

	# Add random reviews
	all_prods = Products.query.all()
	for p in all_prods:
		for i in range(3):
			rat_rev = random.choice(reviews_ratings)
			review = Reviews(product=p, review_string=rat_rev[0], rating=rat_rev[1], status="PROCESSED")
			db.session.add(review)
	db.session.commit()
print("All reviews added")

