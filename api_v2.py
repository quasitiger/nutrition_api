from flask import Response, Flask, g, request, app
from flask_restful import Resource, reqparse

import json

class Food(Resource):

    def __init__(self):
        #self.rows = ["id", "food_cd", "group_name", "good_name", "research_year", "maker_name", "ref_name", "serving_size", "calorie", "carbohydrate", "protein", "province", "sugers", "salt", "cholesterol", "saturated_fatty_acides", "trans_fat"]
        #self.req_args = ['food_name', 'research_year', 'maker_name', 'food_code']
        self.req_args = ["food_cd", "group_name", "food_name", "research_year", "maker_name", "ref_name", "serving_size", "calorie", "carbohydrate", "protein", "province", "sugers", "salt", "cholesterol", "saturated_fatty_acides", "trans_fat"]
    # 조회
    def get(self):

        """
        Read Food informations
        ---
        parameters:
          - name: food_name
            in: query
            type: string
            required: false
            description: Name of the food

          - name: research_year
            in: query
            type: integer
            required: false
            description: The year of research.

          - name: maker_name
            in: query
            type: string
            required: false
            description: The name of the maker.

          - name: food_code
            in: query
            type: string
            required: false
            description: The code of the food.

        responses:
          200:
            description: Success to Retrive Data.

          404:
            description: Data not Found
        """

        # args = immutable dict
        # food_name = request.args.get('food_name')
        # research_year = request.args.get('research_year')
        # maker_name = request.args.get('maker_name')
        # food_code = request.args.get('food_code')
        
        sub_query = ""
        for arg in request.args:
            if arg.replace('food_code','food_cd') in self.req_args:
                sub_query += f"{arg}='{request.args[arg]}'& "

        sub_query = sub_query[0:-2].replace("&","AND").replace("food_code","food_cd")


        query = f"SELECT * FROM data WHERE {sub_query}"
        cur = g.db.execute(query)
        #g.db.commit()
        res = cur.fetchall()

        if res:
            # Response로 만들어서 날려야 유니코드로 인코딩이 깨지는 현상이 없음
            #res2 = Response(json.dumps(dict(res), ensure_ascii=False), status=200)
            res2 = Response(json.dumps( [dict(ix) for ix in res], ensure_ascii=False ), status=200)
            
            # Response 에서 응답코드 변경하려면..
            return res2
        
        else:
            return {"message":"Data not Found"}, 404
    
    # 생성
    def post(self):

        """
        Create Food informations
        ---
        parameters:
          - name: food_name
            in: query
            type: string
            required: false
            description: Name of the food

          - name: research_year
            in: query
            type: integer
            required: false
            description: The year of research.

          - name: maker_name
            in: query
            type: string
            required: false
            description: The name of the maker.

          - name: food_code
            in: query
            type: string
            required: false
            description: The code of the food.

        responses:
          201:
            description: Success to Data Insert.

          400:
            description: Missing Name Field or Invalid Data Format or Parameter
        """

        if not request.json:
            return {'message': 'Bad Request: Missing name field'}, 400

        # food_name = request.json.get('food_name')
        # research_year = request.json.get('research_year')
        # maker_name = request.json.get('maker_name')
        # food_code = request.json.get('food_code')

        # data = []
        # if food_name:
        #     data.append(food_name)
        # else:
        #     data.append(None)

        # if research_year:
        #     data.append(research_year)
        # else:
        #     data.append(None)

        # if maker_name:
        #     data.append(maker_name)
        # else:
        #     data.append(None)

        # if food_code:
        #     data.append(food_code)
        # else:
        #     data.append(None)

        sub_query = ""
        data = []
        for arg in request.json:
            if arg.replace('food_code','food_cd') in self.req_args:
                sub_query += f"{arg}, "
                data.append(request.json.get(arg))

        sub_query = sub_query[0:-2].replace("food_code","food_cd")

        if not data:
            return {"message":"bad request"}, 400

        # 데이터 입력도 인자 네개만..?
        #query = f"INSERT INTO data (food_name, research_year, maker_name, food_cd) VALUES {'('+'?'*len(data)}"
        query = f"INSERT INTO data ({sub_query}) VALUES {'('+'?,'*(len(data)-1)+'?)'}"
        g.db.execute(query, data)
        g.db.commit()


        #query = f"INSERT data ({','.join(self.rows[1:])}) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) "
        #cursor.execute(query, data)
        
        # response OK.. 데이터까지 같이 전송..
        return {"message":"Data Insert Success"},201        

    # 업데이트
    def put(self):

        """
        Update Food informations
        ---
        parameters:
          - name: id
            in: query
            type: integer
            required: true
            description: primary key of the data

          - name: food_name
            in: query
            type: string
            required: false
            description: Name of the food

          - name: research_year
            in: query
            type: integer
            required: false
            description: The year of research.

          - name: maker_name
            in: query
            type: string
            required: false
            description: The name of the maker.

          - name: food_code
            in: query
            type: string
            required: false
            description: The code of the food.

        responses:
          200:
            description: Success to Data Update.

          400:
            description: Missing Name Field or Invalid Data Format or Parameter

          404:
            description: Data not Found
        """

        if not request.json:
            return {'message': 'Bad Request: Missing id field'}, 400

        #PK로 조회

        # PK가 없으면
        id = request.json.get('id')
        if not id:
            return {'message': 'Bad Request: Missing id field'}, 400

        query = f"SELECT * FROM data WHERE id='{request.json.get('id')}'"
        cur = g.db.execute(query)
        res = cur.fetchone()

        # 데이터가 없으면 404 리턴
        if not res:
            return {"message":"Data not Found"}, 404

        # 있으면 업데이트
        sub_query = ""
        for arg in request.json:
            if arg.replace('food_code','food_cd') in self.req_args:
                sub_query += f"{arg}='{request.json.get(arg)}', "

        if not sub_query:
            return {"message":"bad request"}, 400

        #sub_query = sub_query[0:-2].replace("&","AND").replace("food_code","food_cd")
        sub_query = sub_query[0:-2].replace("food_code","food_cd")

        query = f"UPDATE data SET {sub_query} WHERE id='{id}'"
        cur = g.db.execute(query)
        res = g.db.commit()

        query = f"SELECT * FROM data WHERE id='{id}'"
        cur = g.db.execute(query)
        res = cur.fetchone()


        res2 = Response(json.dumps(dict(res), ensure_ascii=False ), status=200)
        return res2
    
        # sub_query = ""
        # for arg in request.json:
        #     if arg in self.req_args:
        #         sub_query += f"{arg}='{request.json.get(arg)}'& "

        # if not sub_query:
        #     return {"message":"bad request"}, 400

        # sub_query = sub_query[0:-2].replace("&","AND").replace("food_code","food_cd")

        # # 해당 데이터가 존재하는지 확인
        # query = f"SELECT * FROM data WHERE {sub_query}"
        # cur = g.db.execute(query)
        # res = cur.fetchall()

        # # 데이터가 없으면 없데이트
        # if not res:
        #         return {"message":"Data not Found"}, 404

        # # 데이터가 있으면.. 여러개있으면.. 수정하는 기준이 있어야할것 같은데..
        # # 위에서 조건에 일치하는 항목을 조회해서 업데이트를 하는게 의미 없을 것 같음.. pk는..
        # sub_query1 = ""
        # sub_query2 = ""
        # query = "Update data SET WHERE"

        # return 200

    # 삭제
    def delete(self):
        """
        Delete Food informations
        ---
        parameters:
          - name: id
            in: query
            type: integer
            required: true
            description: primary key of the data

        responses:
          204:
            description: Success to Delete Update.

          400:
            description: Missing Name Field or Invalid Data Format or Parameter

          404:
            description: Data not Found
        """

        if not request.json:
            return {'message': 'Bad Request: Missing id field'}, 400

        id = request.json.get('id')
        if not id:
            return {'message': 'Bad Request: Missing id field'}, 400

        # 해당 데이터가 존재하는지 확인
        query = f"SELECT * FROM data WHERE id='{id}'"
        cur = g.db.execute(query)
        res = cur.fetchall()

        # 데이터가 없으면 삭제 x
        if not res:
            return {"message":"data not found"}, 404
        
        query = f"DELETE FROM data WHERE id='{id}'"
        cur = g.db.execute(query)
        g.db.commit()

        # 성공 시 204 리턴
        return {"message":"data deleted"}, 204

        # sub_query = ""
        # for arg in request.json:
        #     if arg in self.req_args:
        #         sub_query += f"{arg}='{request.json.get(arg)}'& "

        # if not sub_query:
        #     return {"message":"bad request"}, 400

        # sub_query = sub_query[0:-2].replace("&","AND").replace("food_code","food_cd")

        # # 해당 데이터가 존재하는지 확인
        # query = f"SELECT * FROM data WHERE {sub_query}"
        # cur = g.db.execute(query)
        # res = cur.fetchall()

        # # 데이터가 없으면 삭제 x
        # if not res:
        #     return {"message":"data not found"}, 404

        # # 쿼리 실행부분 예외처리는..
        # # 삭제할 때 데이터 전부 일치하는 항목을 삭제할건지.. 하나만할건지..
        # query = f"DELETE FROM data WHERE {sub_query}"
        # cur = g.db.execute(query)
        # g.db.commit()

        # # 성공 시 204 리턴
        # return 204
        
    

class FoodNameLists(Resource):
    def get(self):
            
        """
        Read Food name informations
        ---
        responses:
          200:
            description: Success to Retrive Data.

          404:
            description: Data not Found
        """

        query = "SELECT food_name FROM data"
        cur = g.db.execute(query)
        res = cur.fetchall()
        #print(res)
        if res:
            res2 = Response(json.dumps( [dict(ix) for ix in res], ensure_ascii=False ), status=200)
            return res2
        else:
            return {"message":"data not found"}, 404

class ResearchYearLists(Resource):
    def get(self):

        """
        Read Research Year informations
        ---
        responses:
          200:
            description: Success to Retrive Data.

          404:
            description: Data not Found
        """

        query = "SELECT research_year FROM data"
        cur = g.db.execute(query)
        res = cur.fetchall()
        #print(res)
        if res:
            res2 = Response(json.dumps( [dict(ix) for ix in res], ensure_ascii=False ), status=200)
            return res2
        else:
            return {"message":"data not found"}, 404
            
class MakerNameLists(Resource):
    def get(self):
        
        """
        Read Maker Name informations
        ---
        responses:
          200:
            description: Success to Retrive Data.

          404:
            description: Data not Found
        """

        query = "SELECT maker_name FROM data"
        cur = g.db.execute(query)
        res = cur.fetchall()
        #print(res)
        if res:
            res2 = Response(json.dumps( [dict(ix) for ix in res], ensure_ascii=False ), status=200)
            return res2
        else:
            return {"message":"data not found"}, 404

class FoodCodeLists(Resource):
    def get(self):
        
        """
        Read Food Code informations
        ---
        responses:
          200:
            description: Success to Retrive Data.

          404:
            description: Data not Found
        """

        query = "SELECT food_cd FROM data"
        cur = g.db.execute(query)
        res = cur.fetchall()
        #print(res)
        if res:
            res2 = Response(json.dumps( [dict(ix) for ix in res], ensure_ascii=False ), status=200)
            return res2
        else:
            return {"message":"data not found"}, 404