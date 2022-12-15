"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Person, Planet


# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/user', methods=['GET'])
def handl_hello():

    users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), users))

    return jsonify(all_users), 200


@app.route('/person', methods=['GET'])
def handle_hello():

    people = Person.query.all()
    all_people = list(map(lambda x: x.serialize(), people))

    return jsonify(all_people), 200


@app.route('/planet', methods=['GET'])
def hand_hello():

    planets = Planet.query.all()
    all_planets = list(map(lambda x: x.serialize(), planets))

    return jsonify(all_planets), 200


@app.route('/person/<int:person_id>', methods=['DELETE'])
def delete_person(person_id):
 person1 = person.query.get(person_id)
 if person1 is None:
  raise APIException("person not found",status_code=404)
 db.session.delete(person1)
 db.session.commit()

 return jsonify("ok"), 200

 #   if person is none:
#    person1 = People.query.get(person_id)
  #   print("This is the position to delete: ", position)
 #   db.session.delete(person1)
  #  return jsonify("deleted")
#

@app.route('/user', methods=["POST"])
def create_user():
    request_body_user = request.get_json()
    user1 = User(email=request_body_user["email"], password=request_body_user["password"])
    db.session.add(user1)
    db.session.commit
    request_body_user = request.get_json()

    return jsonify(request_body_user) , 200

@app.route('/person', methods=["POST"])
def create_person():
    request_body_person = request.get_json()
    person1 = Person(first_name=request_body_person["first_name"], last_name=request_body_person["last_name"])
    db.session.add(person1)
    db.session.commit
    request_body_person = request.get_json()

    return jsonify(request_body_person) , 200

@app.route('/planet', methods=["POST"])
def create_planet():
    request_body_planet = request.get_json()
    planet1 = Planet(planet_name=request_body_planet["planet_name"], planet_size=request_body_planet["planet_size"])
    db.session.add(planet1)
    db.session.commit
    request_body_planet = request.get_json()

    return jsonify(request_body_planet) , 200

@app.route('/user/<int:user_id>', methods=["DELETE"])
def delete_user(user_id):
    raise APIException("User not found", status_code=404)
   # planet1 = Planet(planet_name=request_body_planet["planet_name"], planet_size=request_body_planet["planet_size"])
    db.session.delete(user1)
    db.session.commit
   # request_body_planet = request.get_json()

    return jsonify("deleted") , 200
    
    

# @app.route('/person', methods=["POST"])
# def add_person():
#     print("i'm here")
#     print(request)
#     first_name = request.json[0]['first_name']
#     last_name = request.json[0]['last_name']

#     person = Person(
#         first_name = first_name,
#         last_name = last_name,
#        # is_active = False
#     )

#     person.create()

#     return jsonify(person.serialize())

# @app.route('/planet', methods=["POST"])
# def create_planet():
#     request_body_planet = request.get_json()
#     print(request_body_planet)
#     return jsonify(request_body_planet), 200

#@app.route('/user', methods=['POST'])
#def add_user():
 #   request_body_user = request.get_json() 
  #  user1 = Users(email=request_body_user["email"], password=request_body_user["password"])
#
 #   db.session.add(user1)
  #  db.session.commit()
    
   # return jsonify(request_body_user), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
