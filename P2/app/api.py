import json
from flask_restful import Resource, Api, reqparse
from flask import  jsonify, request
from pymongo import MongoClient
from bson import ObjectId
from app import app

#app = Flask(__name__)
api = Api(app)

# Conectar al servicio (docker) "mongo" en su puerto estandar
client = MongoClient("mongo", 27017) 

# Base de datos
db = client.cockteles   

recipe_parser = reqparse.RequestParser()
recipe_parser.add_argument("name", type=str, help="El nombre es requerido" ,required=True)
recipe_parser.add_argument("slug", type=str)
recipe_parser.add_argument("ingredients", action='append', help="La lista de ingredientes es requerida" ,required=True)
recipe_parser.add_argument("instructions", type=str, action='append' ,help="Las instrucciones son requeridas" ,required=True)


put_parser = reqparse.RequestParser()
put_parser.add_argument("$set", type=json ,help="El nombre es requerido" ,required=True)


#<----------------------------------------------------------------------------------------------------------------------------------->
# para devolver una lista (GET), o añadir (POST)
class RecipeList(Resource):
    def get(self):
        lista = []
        buscados = db.recipes.find().sort('name')
        for recipe in buscados:
            recipe['_id'] = str(recipe['_id']) # paso a string
            lista.append(recipe)
        return jsonify(lista)

    def post(self):
        args = recipe_parser.parse_args()
        result = db.recipes.insert_one(args)
        return str(result.inserted_id), 201


#<----------------------------------------------------------------------------------------------------------------------------------->
class Recipe(Resource):
    def get(self, id):
        buscado = db.recipes.find_one({'_id':ObjectId(id)})
        if buscado:
            buscado['_id'] = str(buscado['_id'])
            return jsonify(buscado)
        else:
            return jsonify({'error':'Not found'})

    def put(self, id):
        args = request.get_json()
        result = db.recipes.update_one({'_id':ObjectId(id)}, args)

        if(result.matched_count==1):
            modificado = db.recipes.find_one({'_id':ObjectId(id)})
            modificado['_id'] = str(modificado['_id'])
            return jsonify(modificado)
        else:
            return jsonify({'error':'Not found'})

    def delete(self, id):
        result = db.recipes.delete_one({'_id':ObjectId(id)})

        if(result.deleted_count==1):
            return id
        else:
            return jsonify({'error':'Not found'})


api.add_resource(RecipeList,'/RecipeList')
api.add_resource(Recipe,'/Recipe/<id>')


if __name__ == "__main__":
    app.run(debug=True)
