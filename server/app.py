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
        plants = Plant.query.all()
        plant_list = []

        for plant in plants:
            plant_data = {
                'id': plant.id,
                'name': plant.name,
                'image': plant.image,
                'price': float(plant.price)
            }
            plant_list.append(plant_data)

        response = make_response(
            plant_list,
            200,
        )
        return response
        # return jsonify(plant_list)
    
    def post(self):
        data = request.get_json()
        if 'name' not in data or 'image' not in data or 'price' not in data:
            response = make_response(
                {"message": "Please provide values for 'name', 'image', and 'price'."},
                400,
            )
            return response

        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price']
        )

        db.session.add(new_plant)
        # db.session.commit()
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            response = make_response(
                {"message": f"Failed to create the plant. Error: {str(e)}"},
                500,
            )

            return response
        response = make_response(
            new_plant.to_dict(),
            201,
        )

        return response
    
api.add_resource(Plants, '/plants')

class PlantByID(Resource):
    def get(self,id):
        plant= Plant.query.get(id)
        if plant:
            plant_data = {
                'id':plant.id,
                'name':plant.name,
                'image':plant.image,
                'price': float(plant.price)
            }

            response = make_response(
                plant_data,
                200,
            )
        else: 
            response = make_response(
                {"message": f"Plant {id} not found."},
                404,
            )
        return response

api.add_resource(PlantByID, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
