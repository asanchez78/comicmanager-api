from db import db


class SeriesModel(db.Model):
    __tablename__ = 'series'

    series_id = db.Column(db.Integer, primary_key=True)
    publisherID = db.Column(db.Integer, db.ForeignKey('publishers.publisherID'))
    series_name = db.Column(db.String(100))
    series_vol = db.Column(db.Integer)
    cvVolumeID = db.Column(db.Integer)
    apiDetailURL = db.Column(db.String(255))
    siteDetailURL = db.Column(db.String(255))
    comics = db.relationship('ComicModel', lazy='dynamic')

    def __init__(self, series_name, series_vol, publisherID, cvVolumeID, apiDetailURL, siteDetailURL):
        self.series_name = series_name
        self.series_vol = series_vol
        self.publisherID = publisherID
        self.cvVolumeID = cvVolumeID
        self.apiDetailURL = apiDetailURL
        self.siteDetailURL = siteDetailURL

    def json(self, list_comics):
        if list_comics:
            return {'series_id': self.series_id,
                    'series': self.series_name,
                    'volume': self.series_vol,
                    'publisher': self.publisherID,
                    'comicvine id': self.cvVolumeID,
                    'api url': self.apiDetailURL,
                    'site url': self.siteDetailURL,
                    'comics': [comic.json() for comic in self.comics.all()]}

        return {'series_id': self.series_id,
                'series': self.series_name,
                'volume': self.series_vol,
                'publisher': self.publisherID,
                'comicvine id': self.cvVolumeID,
                'api url': self.apiDetailURL,
                'site url': self.siteDetailURL}

    @classmethod
    def find_by_name(cls, series_name, series_vol):
        return cls.query.filter_by(series_name=series_name, series_vol=series_vol).first()

    @classmethod
    def find_by_id(cls, series_id):
        return cls.query.filter_by(series_id=series_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
