# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Pet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Welcome to the pet directory!'}
    return make_response(body, 200)

# creating a route id of finding pets by id using to_dict method
@app.route("/pets/<int:id>")
def pet_by_id(id):
    #querying the pet and finding it by the id 
    pet = Pet.query.filter(Pet.id == id).first()

    # an if statement to check whether the id exists or not
    if pet:
        body = pet.to_dict()
        status = 200
    else:
        body ={
            "message" : f"Pet {id} not found"
        }
        status = 404
    response = make_response(body, status)
    return response

@app.route("/species/<string:species>")
def pet_by_species(species):
    # initializing pets with an empty list
    pets = []

    # querying pets by the species, looping through the pets and appeding the pets to the pets list
    for pet in Pet.query.filter_by(species = species).all():
        pets.append(pet.to_dict())
    
    body = {
        "Count": len(pets),
        "pets" : pets
    }
    status = 200
    response = make_response(body, status)
    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)
