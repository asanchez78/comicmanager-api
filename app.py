from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister, UsersComics
from resources.comic import Comic, ComicList
from resources.series import Series, SeriesList
from resources.publisher import Publisher, PublisherList
from resources.comicvinesearch import ComicvineSeriesSearch, ComicvineComicSearch
from datetime import timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@127.0.0.1/comicdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['BUNDLE_ERRORS'] = True
app.secret_key = 'test'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


app.config['JWT_AUTH_URL_RULE'] = '/v1/auth'
#  config JWT to expire within half an hour
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=7200)

jwt = JWT(app, authenticate, identity)  # /auth


api.add_resource(Comic, '/v1/comic/')
api.add_resource(ComicList, '/v1/comics/')
api.add_resource(Series, '/v1/series/')
api.add_resource(SeriesList, '/v1/serieslist/')
api.add_resource(Publisher, '/v1/publisher/')
api.add_resource(PublisherList, '/v1/publishers/')
api.add_resource(UserRegister, '/v1/register')
api.add_resource(UsersComics, '/v1/user/comics/')
api.add_resource(ComicvineSeriesSearch, '/v1/comicvinesearch/series/')
api.add_resource(ComicvineComicSearch, '/v1/comicvinesearch/comic/')


if __name__ == '__main__':
    from db import db

    db.init_app(app)
    app.run(port=5000, debug=True)
