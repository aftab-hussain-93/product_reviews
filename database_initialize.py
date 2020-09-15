import pandas as pd
import re, random, uuid
from app import db, app
from models import Products, Reviews, Ratings
from utils import check_threshold, update_rating_score, review_evaluation

df = pd.read_csv('data/flipkart_com-ecommerce_sample.csv', usecols=['product_name','image'])
df = df.sample(frac=1).reset_index(drop=True)
data = df.head(300)
sample_reviews = [('Really good',4), ('Excellent', 5), ('Average',3), ('Bad', 2), ('Horrible', 1) ]
all_products = []
for index,row in data.iterrows():
	result = re.search(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))", row["image"])
	image = result.group(1)
	name = row["product_name"]
	all_products.append({"name": name, "image": image })

print("All product details extracted from CSV file")

with app.app_context():
	# Inital setup. Create DB and Add all products.
	db.create_all()
	for prod in all_products:
		p = Products(name = prod['name'], image_url = prod['image'], public_key = uuid.uuid4().hex )
		db.session.add(p)
	db.session.commit()
	print("All products are added.")

	# Creating all sample reviews.
	prods = Products.query.all()
	for p in prods:
		for i in range(random.randint(1,9)):
			rat_rev = random.choice(sample_reviews)
			review = Reviews(product=p, review_string=rat_rev[0], rating=rat_rev[1], status="PROCESSED")
			db.session.add(review)
	db.session.commit()
	print("All reviews are added")

	print("Initial update of the rating score for each product")
	prod_ids = [p.id for p in prods]
	prod_overall_rating = review_evaluation(prod_ids)
	update_rating_score(prod_overall_rating)
	print("Rating score initalized")



