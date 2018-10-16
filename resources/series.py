from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.series import SeriesModel


class Series(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('series_id',
                        type=str,
                        # required=True,
                        help='series_name cannot be blank')

    parser.add_argument('series_name',
                        type=str,
                        # required=True,
                        help='series_name cannot be blank')

    parser.add_argument('series_vol',
                        type=str,
                        help='series_vol cannot be blank')
    parser.add_argument('publisherID',
                        type=str,
                        help='publisher id cannot be blank')
    parser.add_argument('ccVolumeID',
                        type=str,
                        help='ccVolumeID cannot be blank')
    parser.add_argument('apiDetailURL',
                        type=str,
                        help='apiDetailURL cannot be blank')
    parser.add_argument('siteDetailURL',
                        type=str,
                        help='siteDetailURL cannot be blank')

    parser.add_argument('list_comics',
                        type=bool,
                        # required=True,
                        help='series_name cannot be blank')

    def get(self):
        data = Series.parser.parse_args()
        series = SeriesModel.find_by_id(data['series_id'])
        if series:
            return series.json(list_comics=True)
        return {'message': 'Series not Found'}

    @jwt_required()
    def post(self):
        data = Series.parser.parse_args()

        if SeriesModel.find_by_name(data['series_name'], data['series_vol']):

            return {'message': "A series with name '{}' and volume '{}' already exists."
                    .format(data['series_name'], data['series_vol'])}, 400

        series = SeriesModel(data['series_name'], data['series_vol'], data['publisherID'], data['ccVolumeID'],
                             data['apiDetailURL'], data['siteDetailURL'])
        try:
            series.save_to_db()
        except:
            return {'message': 'An error occurred while creating the series'}, 500

        return series.json(list_comics=False), 201

    @jwt_required()
    def delete(self):
        data = Series.parser.parse_args()
        series = SeriesModel.find_by_id(data['series_id'])
        if series:
            series.delete_from_db()

        return {'message': 'Series deleted'}


class SeriesList(Resource):
    def get(self):
        return {'series': [series.json(list_comics=False) for series in SeriesModel.query.all()]}
