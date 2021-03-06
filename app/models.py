import re
from app import db
from app.general_utilities import calculate_rating_string 

class Base(db.Model):
	__abstract__ = True

	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
	date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class Products(Base):
	name = db.Column(db.String, nullable=False)
	image_url = db.Column(db.String)
	public_key = db.Column(db.String, unique=True, nullable=False)
	rating = db.relationship('Ratings', backref='product', lazy=True) 
	review = db.relationship('Reviews', backref='product', lazy=True) 

	@classmethod
	def get_all_products(cls):
		return [{"name":prod.name, "public_key":prod.public_key} for prod in cls.query.all()]

	def __repr__(self):
		return "Product {} - {}".format(self.name, self.image_url)

	def __str__(self):
		return f"{self.name}"

class Reviews(Base):
	product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
	review_string = db.Column(db.String, nullable=False)
	rating = db.Column(db.Integer, nullable=False)
	status = db.Column(db.String, default='NEW') #Valid statuses - NEW, PROCESSED, EVALUATING(?)

	def __repr__(self):
		return "Review {} - {}".format(self.review_string, self.rating)

	def __str__(self):
		return f"{self.review_string} - {self.rating}"

class Ratings(Base):
	"""
	Consists of the overall rating of each product.
	"""
	product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False, unique=True)
	rating_score = db.Column(db.String, nullable=False)

	@property
	def rating_string(self):
		rating_values = re.findall(r'\d+', self.rating_score)
		rating_values = list(map(int, rating_values))
		return calculate_rating_string(rating_values)

	def __repr__(self):
		return "Rating {} - {}".format(self.product_id, self.rating_string)

	def __str__(self):
		return f"Rating string {self.rating_string}"

