class Config:
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SQLALCHEMY_DATABASE_URI = r"sqlite:///test.db"
	SECRET_KEY = 'secret key'