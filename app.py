from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister, UsersComics
from resources.comic import Comic, ComicList
from resources.series import Series, SeriesList
from resources.publisher import Publisher, PublisherList
from resources.comicvinesearch import ComicvineSeriesSearch, ComicvineComicSearch

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


# app.config['JWT_AUTH_URL_RULE'] = '/login'
#  config JWT to expire within half an hour
# app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)

jwt = JWT(app, authenticate, identity)  # /auth


api.add_resource(Comic, '/comic/')
api.add_resource(ComicList, '/comics/')
api.add_resource(Series, '/series/')
api.add_resource(SeriesList, '/serieslist/')
api.add_resource(Publisher, '/publisher/')
api.add_resource(PublisherList, '/publishers/')
api.add_resource(UserRegister, '/register')
api.add_resource(UsersComics, '/user/comics/')
api.add_resource(ComicvineSeriesSearch, '/comicvinesearch/series/')
api.add_resource(ComicvineComicSearch, '/comicvinesearch/comic/')


if __name__ == '__main__':
    from db import db

    db.init_app(app)
    app.run(port=5000, debug=True)
