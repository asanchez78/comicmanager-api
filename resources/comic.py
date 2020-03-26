from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.comic import ComicModel


class Comic(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('comic_id', type=int, help="This field cannot be blank")
    parser.add_argument('series_id', type=int, help="This field cannot be blank")
    parser.add_argument('issue_number', type=str, help="This field cannot be blank")
    parser.add_argument('story_name', type=str, help="This field cannot be blank")
    parser.add_argument('release_date', type=str, help="This field cannot be blank")
    parser.add_argument('plot', type=str, help="This field cannot be blank")
    parser.add_argument('cover_image', type=str, help="This field cannot be blank")
    parser.add_argument('wiki_id', type=str, help="This field cannot be blank")
    parser.add_argument('wikiUpdated', type=str, help="This field cannot be blank")

    @jwt_required()
    def get(self):
        data = Comic.parser.parse_args()

        comic = ComicModel.find_by_id(data['comic_id'])
        if comic:
            return comic.json()
        return {"message": "Comic not found"}, 404

    @jwt_required()
    def post(self):
        data = Comic.parser.parse_args()

        if ComicModel.find_by_series(data['series_id'], data['issue_number']):
            return {"message": "Series id '{}' issue number '{}' already exists.".
                    format(data['series_id'], data['issue_number'])}, 400

        comic = ComicModel(data['series_id'], data['issue_number'], data['story_name'], data['release_date'],
                           data['plot'], data['cover_image'], data['wiki_id'], data['wikiUpdated'])

        try:
            comic.save_to_db()
        except:
            return {"message": "An error occurred inserting the comic."}, 500

        return comic.json(), 201

    @jwt_required()
    def delete(self):
        data = Comic.parser.parse_args()
        comic = ComicModel.find_by_id(data['comic_id'])
        if comic:
            comic.delete_from_db()

        return {"message": "Comic deleted"}

    @jwt_required()
    def put(self):

        data = Comic.parser.parse_args()

        comic = ComicModel.find_by_id(data['comic_id'])

        if comic is None:
            comic = ComicModel(data['series_id'], data['issue_number'], data['story_name'], data['release_date'],
                               data['plot'], data['cover_image'], data['wiki_id'], data['wikiUpdated'])
        else:
            comic.plot = data['plot']
        comic.save_to_db()

        return comic.json()


class ComicList(Resource):
    @jwt_required()
    def get(self):
        return {'comics': [comic.json() for comic in ComicModel.query.all()]}
