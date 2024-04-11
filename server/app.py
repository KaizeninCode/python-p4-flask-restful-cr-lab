#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        plants_dict_list = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(plants_dict_list, 200)

    def post(self):
        ## The post method now checks request.json instead of request.form since the test is sending JSON data.
        
         # Check if all required form fields are present
        required_fields = ['name', 'image', 'price']
        if not all(field in request.json for field in required_fields):
            return make_response({'error': 'Missing required fields'}, 400)

    # Check if any required field has a None value
        if any(request.json[field] is None for field in required_fields):
            return make_response({'error': 'Required fields cannot be None'}, 400)
        
        new_record = Plant(
        name=request.json['name'],
        image=request.json['image'],
        price=request.json['price'],
    )

        db.session.add(new_record)
        db.session.commit()

        response_dict = new_record.to_dict()

        return make_response(response_dict, 201)
    
api.add_resource(Plants, '/plants')    

class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.filter_by(id=id).first()
        if plant:
            response_dict = plant.to_dict()
            return make_response(response_dict, 200)
        else:
            return make_response({'error': 'Plant not found'}, 404)
    
api.add_resource(PlantByID, '/plants/<int:id>')    
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
