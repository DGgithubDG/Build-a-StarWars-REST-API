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


@app.route('/person/<int:id>', methods=['DELETE'])
def delete_person(person_id):
    i = 0
    for person in person:
        if person["person_id"] == person_id:
            person.pop(i)
            i += 1
            return jsonify("")

 #   if person is none:
#    person1 = People.query.get(person_id)
  #   print("This is the position to delete: ", position)
 #   db.session.delete(person1)
  #  return jsonify("deleted")
#

@app.route('/user', methods=["POST"])
def add_user():
    print("i'm here")
    print(request)
    email = request.json[0]['email']
    password = request.json[0]['password']

    user = User(
        email = email,
        password = password,
        is_active = False
    )

    user.create()

    return jsonify(user.serialize())

@app.route('/person', methods=["POST"])
def add_person():
    print("i'm here")
    print(request)
    first_name = request.json[0]['first_name']
    last_name = request.json[0]['last_name']

    person = Person(
        first_name = first_name,
        last_name = last_name,
        is_active = False
    )

    person.create()

    return jsonify(person.serialize())

@app.route('/planet', methods=["POST"])
def add_planet():
    print("i'm here")
    print(request)
    planet_name = request.json[0]['planet_name']
    planet_size = request.json[0]['planet_size']

    planet = Planet(
        planet_name = planet_name,
        planet_size = planet_size,
        is_active = False
    )

    planet.create()

    return jsonify(planet.serialize())

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
