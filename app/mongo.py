from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo import MongoClient


class Mongo:
    def __init__(self, client: MongoClient):
        database = client['the_food_searcher']

        self.user_collection = database['users']

    async def create_user(self, user_id: int, height: float, weight: float, age: float, sex: str, factor: float, plan: int):
        if not self.user_collection.find_one({'_id': user_id}):
            self.user_collection.insert_one({
                '_id': user_id,
                'height': height,
                'weight': weight,
                'age': age,
                'sex': sex,
                'factor': factor,
                'plan': plan
            })
        else:
            print('User already exists')

    async def create_or_update_user(self, user_id: int, height: float, weight: float, age: float, sex: str, factor: float, plan: int):
        self.user_collection.replace_one(
            {'_id': user_id},
            {
                '_id': user_id,
                'height': height,
                'weight': weight,
                'age': age,
                'sex': sex,
                'factor': factor,
                'plan': plan
            },
            upsert=True
        )

    async def get_user_by_id(self, user_id: int):
        return self.user_collection.find_one({'_id': user_id})

    async def delete_user_by_id(self, user_id: int):
        self.user_collection.delete_one({'_id': user_id})
