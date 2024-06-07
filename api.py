from flask import Flask, g
from flask_restful import Api
from flasgger import Swagger
from api_v2 import Food, FoodNameLists, MakerNameLists, ResearchYearLists, FoodCodeLists

import sqlite3

# 데이터베이스 이름
database = 'food_nutrition.db'

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

api_version = 2

## db
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(database, check_same_thread=False)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.before_request
def before_request():
    g.db = get_db()

@app.teardown_request
def teardown_request(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()


## 경로 설정
api.add_resource(Food, f'/v{api_version}/food/')
# list 조회
api.add_resource(FoodNameLists, f'/v{api_version}/foods')
api.add_resource(MakerNameLists, f'/v{api_version}/makers')
api.add_resource(ResearchYearLists, f'/v{api_version}/years')
api.add_resource(FoodCodeLists, f'/v{api_version}/codes')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=3000)