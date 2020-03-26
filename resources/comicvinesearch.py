from flask_restful import Resource, reqparse
import requests
from flask_jwt import jwt_required


class ComicvineSearchParser:
    series_search_parser = reqparse.RequestParser()
    series_search_parser.add_argument('series_name', type=str, required=True, help="series_name cannot be blank")
    series_search_parser.add_argument('cvapi_key', type=str, required=True,
                                      help="A comicvine API key is required to use this endpoint")

    comic_search_parser = series_search_parser.copy()
    comic_search_parser.add_argument('comicvine_id', type=str, required=True, help="comicvine_id cannot be blank")
    comic_search_parser.add_argument('issue_number', type=str, required=True, help="issue_number cannot be blank")
    comic_search_parser.remove_argument('series_name')


class ComicvineSeriesSearch(Resource):

    headers = {
        'User-Agent': 'Wade Wilson'
    }

    @jwt_required()
    def get(self):
        data = ComicvineSearchParser.series_search_parser.parse_args()
        cvapi_key = data['cvapi_key']
        series_name = data['series_name']
        api_url = "https://comicvine.gamespot.com/api/volumes/?api_key={}&" \
                  "filter=name:{}&format=json&" \
                  "field_list=id,name,start_year,site_detail_url,api_detail_url,image,count_of_issues"\
            .format(cvapi_key, series_name)
        response = requests.get(api_url, headers=self.headers).json()
        return response


class ComicvineComicSearch(Resource):

    @jwt_required()
    def get(self):
        data = ComicvineSearchParser.comic_search_parser.parse_args()
        comicvine_id = data['comicvine_id']
        issue_number = data['issue_number']
        cvapi_key = data['cvapi_key']

        api_url = "http://comicvine.gamespot.com/api/issues/?filter=volume:{},issue_number:{}&" \
                  "format=json&api_key={}".format(comicvine_id, issue_number, cvapi_key)
        response = requests.get(api_url, headers=ComicvineSeriesSearch.headers).json()
        return response

