from db import db


class PublisherModel(db.Model):
    __tablename__ = 'publishers'
    publisherID = db.Column(db.Integer, primary_key=True)
    publisherName = db.Column(db.String(50))
    publisherShort = db.Column(db.String(50))
    series = db.relationship('SeriesModel', lazy='dynamic')

    def __init__(self, publisher_name, publisher_short):
        self.publisherName = publisher_name
        self.publisherShort = publisher_short

    def json(self):
        return {
            'publisher_id': self.publisherID,
            'publisherName': self.publisherName,
            'publisherShort': self.publisherShort,
            'series': [series.json(list_comics=False) for series in self.series.all()]
        }

    @classmethod
    def find_by_id(cls, publisher_id):
        return cls.query.filter_by(publisherID=publisher_id).first()

    @classmethod
    def find_by_name(cls, publisher_name):
        return cls.query.filter_by(publisherName=publisher_name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
