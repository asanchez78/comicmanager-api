from db import db


class ComicModel(db.Model):
    __tablename__ = 'comics'

    comic_id = db.Column(db.Integer, primary_key=True)
    series_id = db.Column(db.Integer, db.ForeignKey('series.series_id'))
    series = db.relationship('SeriesModel')
    issue_number = db.Column(db.Integer)
    story_name = db.Column(db.String(200))
    release_date = db.Column(db.String(30))
    plot = db.Column(db.String(1000))
    cover_image = db.Column(db.String(255))
    wiki_id = db.Column(db.Integer)
    wikiUpdated = db.Column(db.Integer)

    def __init__(self, series_id, issue_number, story_name, release_date, plot, cover_image, wiki_id,
                 wiki_updated):
        self.series_id = series_id
        self.issue_number = issue_number
        self.story_name = story_name
        self.release_date = release_date
        self.plot = plot
        self.cover_image = cover_image
        self.wiki_id = wiki_id
        self.wikiUpdated = wiki_updated

    def json(self):
        return {'comic_id': self.comic_id,
                'series_id': self.series_id,
                # 'series_name': self.series_name,
                'issue_number': self.issue_number,
                'story_name': self.story_name,
                'release_date': self.release_date,
                'plot': self.plot,
                'cover_image': self.cover_image,
                'wiki_id': self.wiki_id,
                'wikiUpdated': self.wikiUpdated
                }

    @classmethod
    def find_by_id(cls, comic_id):
        return cls.query.filter_by(comic_id=comic_id).first()

    @classmethod
    def find_by_series(cls, series_id, issue_number):
        return cls.query.filter_by(series_id=series_id, issue_number=issue_number).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
