from flask_restful import Resource, reqparse
from models.user import UserModel
import json
from models.comic import ComicModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="username cannot be left blank!"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="password cannot be left blank!"
                        )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "User already exists"}, 400

        user = UserModel(**data)
        user.save_to_db()

        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "INSERT INTO users VALUES (NULL, ?, ?)"
        # cursor.execute(query, (data['username'], data['password']))
        #
        # connection.commit()
        # connection.close()

        return {"message": "User created successfully."}, 201


class UsersComics(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('user_id',
                        type=int,
                        required=True,
                        help="User ID is required")
    parser.add_argument('comic_id',
                        type=int,
                        help="Comic ID is required")

    def get(self):
        data = UsersComics.parser.parse_args()
        comics = UserModel.find_users_comics(str(data['user_id']))
        return comics
        # return {'comics': [jsonify(comics)]}
