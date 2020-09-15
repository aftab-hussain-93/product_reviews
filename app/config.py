import os

class Config:
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SQLALCHEMY_DATABASE_URI = r"sqlite:///product.db"
	SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'