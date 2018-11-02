import os

SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:root@localhost:3306/movie'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = 'LLa7OxjE0XgTIOYxv1IgxAQ3y9rlmn'
UP_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploads/')

print(os.path.dirname(__file__))
print(os.path.abspath(os.path.dirname(__file__)))
print(UP_DIR)