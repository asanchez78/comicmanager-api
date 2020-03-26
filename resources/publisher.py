from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.publisher import PublisherModel


class Publisher(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('publisher_id', type=int)
    parser.add_argument('publisherName', type=str)
    parser.add_argument('publisherShort', type=str)

    @jwt_required()
    def get(self):
        data = Publisher.parser.parse_args()
        publisher = PublisherModel.find_by_id(data['publisher_id'])
        if publisher:
            return publisher.json()
        return {'message': 'publisher not found'}

    @jwt_required()
    def post(self):
        data = Publisher.parser.parse_args()
        if PublisherModel.find_by_name(data['publisherName']):
            return {'message': 'A publisher with the name {} already exists'.format(data['publisherName'])}, 400

        publisher = PublisherModel(data['publisherName'], data['publisherShort'])

        try:
            publisher.save_to_db()
        except:
            return {'message': 'An error occurred while creating the publisher'}, 500

        return publisher.json()

    @jwt_required()
    def delete(self):
        data = Publisher.parser.parse_args()
        publisher = PublisherModel.find_by_id(data['publisher_id'])
        if publisher:
            publisher.delete_from_db()
        return {'message': 'publisher deleted'}


class PublisherList(Resource):

    @jwt_required()
    def get(self):
        return {'series': [publisher.json() for publisher in PublisherModel.query.all()]}
