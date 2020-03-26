from db import db
import sqlite3

users_comics = db.Table('users_comics',
                        db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
                        db.Column('comic_id', db.Integer, db.ForeignKey('comics.comic_id'), primary_key=True),
                        db.Column('custPlot', db.String(10000)),
                        db.Column('custCover', db.String(255)),
                        db.Column('custStoryName', db.String(255))
                        )


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    user_comics = db.relationship('ComicModel', secondary=users_comics, backref=db.backref('users_comics',
                                                                                           lazy='dynamic'))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM users WHERE username=?"
        # result = cursor.execute(query, (username,))
        # row = result.fetchone()
        # if row:
        #     user = cls(*row)
        # else:
        #     user = None
        #
        # connection.close()
        # return user

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_users_comics(cls, user_id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "select * from comics " \
                "left join series on comics.series_id=series.series_id " \
                "left join users_comics on comics.comic_id=users_comics.comic_id " \
                "where users_comics.user_id=?"
        result = cursor.execute(query, user_id)
        return [dict(zip([key[0] for key in cursor.description], row)) for row in result]
        # return cls.query.filter_by(id=user_id)
