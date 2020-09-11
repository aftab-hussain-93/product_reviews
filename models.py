from app import db

class Base(db.Model):
	__abstract__ = True

	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
	date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class Products(Base):
	name = db.Column(db.String, nullable=False)
	image_url = db.Column(db.String)
	rating_string = db.relationship('Ratings', backref='product', lazy=True) 
	review = db.relationship('Reviews', backref='product', lazy=True) 

	def __repr__(self):
		return "Product {} - {}".format(self.name, self.image_url)

class Reviews(Base):
	product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
	review_string = db.Column(db.String, nullable=False)
	rating = db.Column(db.Integer)
	status = db.Column(db.String, default='NEW') #Valid statuses - NEW, PROCESSED, EVALUATING(?)

	def __repr__(self):
		return "Review {} - {}".format(self.review_string, self.rating)

class Ratings(Base):
	"""
	Consists of the overall rating of each product.
	"""
	product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False, unique=True)
	rating_string = db.Column(db.String, nullable=False, default='000000')

	def __repr__(self):
		return "Rating {} - {}".format(self.product_id, self.rating_string)

