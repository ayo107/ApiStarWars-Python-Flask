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
from models import db, People, Planets, Starships, User, Favorites, PeopleFavorites, PlanetsFavorites, StarshipsFavorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
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


###PEOPLE###

@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    all_people = list(map(lambda people: people.serialize(), people))
    return jsonify(all_people), 201

@app.route('/people', methods=['POST'])
def post_people():
    body = request.get_json()
    print(body)
    people = People(uid=body["uid"], name=body["name"],height=body['height'], mass=body['mass'],hair_color=body['hair_color'],
    homeworld=body['homeworld'], eye_color=body['eye_color'], gender=body['gender'])
    db.session.add(people)
    db.session.commit()
    return jsonify(people.serialize()), 201

@app.route('/people/<int:people_uid>', methods=['GET', 'PUT', 'DELETE'])
def people_single(people_uid):
    if request.method == 'GET':
        people = People.query.get(people_uid)
        if people is None:
            raise APIException("Personaje no encontrado", 404)

        return jsonify(people.serialize())
    
    if request.method == 'PUT':
        print(people_uid)
        people = People.query.get(people_uid)
        print(people)
        if people is None:
           raise APIException("Personaje no encontrado", 404)
        body = request.get_json()

        if not ("uid" in body):
            raise APIException("uid no encontrado", 404)

        people.uid = body["uid"]
        people.name = body["name"]
        people.height = body["height"]
        people.mass = body["mass"]
        people.hair_color = body["hair_color"]
        people.homeworld = body["homeworld"]
        people.eye_color = body["eye_color"]
        people.gender = body["gender"]
        db.session.commit()

        return jsonify(people.serialize())
    
    if request.method == 'DELETE':
        people = People.query.get(people_uid)
        if people is None:
            raise APIException("Personaje no encontrado", 404)
        db.session.delete(people)
        db.session.commit()

        return jsonify(people.serialize())

###PLANETS###

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    all_planets = list(map(lambda planets: planets.serialize(), planets))
    return jsonify(all_planets), 201

@app.route('/planets', methods=['POST'])
def post_planets():
    body = request.get_json()
    print(body)
    planets = Planets(uid=body["uid"], name=body["name"], surface_water=body['surface_water'], terrain=body['terrain'], climate=body['climate'],
    population=body['population'], diameter=body['diameter'])
    db.session.add(planets)
    db.session.commit()
    return jsonify(planets.serialize()), 201


@app.route('/planets/<int:planets_id>', methods=['GET', 'PUT', 'DELETE'])
def planets_single(planets_id):
    if request.method == 'GET':
        planets = Planets.query.get(planets_id)
        if planets is None:
            raise APIException("Planeta no encontrado", 404)

        return jsonify(planets.serialize())
    
    if request.method == 'PUT':
        planets = Planets.query.get(planets_id)
        if planets is None:
           raise APIException("Planeta no encontrado", 404)
        body = request.get_json()

        if not ("uid" in body):
            raise APIException("Parametro no encontrado", 404)

        planets.uid = body["uid"]
        planets.name = body["name"]
        planets.surface_water = body["surface_water"]
        planets.terrain = body["terrain"]
        planets.climate = body["climate"]
        planets.population = body["population"]
        planets.diameter = body["diameter"]
        db.session.commit()

        return jsonify(planets.serialize())
    
    if request.method == 'DELETE':
        planets = Planets.query.get(planets_id)
        if planets is None:
            raise APIException("Planet not found", 404)
        db.session.delete(planets)
        db.session.commit()
        
        return jsonify(planets.serialize())


###STARSHIPS###

@app.route('/starships', methods=['GET'])
def get_starships():
    starships = Starships.query.all()
    all_starships = list(map(lambda starships: starships.serialize(), starships))
    return jsonify(all_starships), 201

@app.route('/starships', methods=['POST'])
def post_starships():
    body = request.get_json()
    print(body)
    starships = Starships(uid=body["uid"], name=body["name"], model=body['model'], cost=body['cost'], cargo_capacity=body['cargo_capacity'],
    passengers=body['passengers'])
    db.session.add(starships)
    db.session.commit()
    return jsonify(starships.serialize()), 201


@app.route('/starships/<int:starships_id>', methods=['GET', 'PUT', 'DELETE'])
def starships_single(starships_id):
    if request.method == 'GET':
        starships = Starships.query.get(starships_id)
        if starships is None:
            raise APIException("Nave no encontrada", 404)

        return jsonify(starships.serialize())
    
    if request.method == 'PUT':
        starships = Starships.query.get(starships_id)
        if starships is None:
           raise APIException("Nave no encontrada", 404)
        body = request.get_json()

        if not ("uid" in body):
            raise APIException("Parametro no encontrado", 404)

        starships.uid = body["uid"]
        starships.name = body["name"]
        starships.model = body["model"]
        starships.cost = body["cost"]
        starships.cargo_capacity = body["cargo_capacity"]
        starships.passengers = body["passengers"]
        db.session.commit()

        return jsonify(starships.serialize())
    
    if request.method == 'DELETE':
        starships = Starships.query.get(starships_id)
        if starships is None:
            raise APIException("Nave no encontrada", 404)
        db.session.delete(starships)
        db.session.commit()
        
        return jsonify(starships.serialize())

###USERS###


@app.route('/users', methods=['GET'])
def get_users():
    user = User.query.all()
    all_users = list(map(lambda user: user.serialize(), user))
    return jsonify(all_users), 201

@app.route('/user', methods=['POST'])
def post_user():
    body = request.get_json()
    print(body)
    user = User(name=body["name"], email=body["email"], password=body["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize()), 201

###FAVORITES###

@app.route('/user/<int:user_id>/favorites/people', methods=['GET'])
def get_people_fav(user_id):
    people_fav = PeopleFavorites.query.filter_by(user_id=user_id)
    if user_id is None:
        return "No hay personajes favoritos"

    userFavorites = list(map(lambda people_fav: people_fav.serialize(), people_fav))
    return jsonify(userFavorites),201

@app.route('/user/<int:user_id>/favorites/people/<int:people_id>', methods=['POST'])
def pe_fav(user_id, people_id):
    favorites = PeopleFavorites(user_id=user_id, people_id=people_id)
    db.session.add(favorites)
    db.session.commit()
    return jsonify(favorites.serialize()), 201

@app.route('/user/<int:user_id>/favorites/people/<int:people_id>', methods=['DELETE'])
def delete_people_fav(user_id, people_id):
    deleteFav = PeopleFavorites.query.filter_by(user_id=user_id, people_id=people_id).one() #one devuelve el objeto encontrado, sin el one, devuelve el queryobject
    db.session.delete(deleteFav)
    db.session.commit()

    return jsonify(deleteFav.serialize()), 202


###FAVORITES PLANETS###

@app.route('/user/<int:user_id>/favorites/planets', methods=['GET'])
def get_planets_fav(user_id):
    planets_fav = PlanetsFavorites.query.filter_by(user_id=user_id)
    if user_id is None:
        return "No hay Planetas favoritos"

    userFavorites = list(map(lambda planets_fav: planets_fav.serialize(), planets_fav))
    return jsonify(userFavorites),201

@app.route('/user/<int:user_id>/favorites/planets/<int:planets_id>', methods=['POST'])
def post_planets_fav(user_id, planets_id):
    favorites = PlanetsFavorites(user_id=user_id, planets_id=planets_id)
    db.session.add(favorites)
    db.session.commit()
    return jsonify(favorites.serialize()), 201

@app.route('/user/<int:user_id>/favorites/planets/<int:planets_id>', methods=['DELETE'])
def delete_planets_fav(user_id, planets_id):
    deleteFav = PlanetsFavorites.query.filter_by(user_id=user_id, planets_id=planets_id).one() #one devuelve el objeto encontrado, sin el one, devuelve el queryobject
    db.session.delete(deleteFav)
    db.session.commit()

    return jsonify(deleteFav.serialize()), 202

###FAVORITES STARSHIPS###

@app.route('/user/<int:user_id>/favorites/starships', methods=['GET'])
def get_starships_fav(user_id):
    starships_fav = StarshipsFavorites.query.filter_by(user_id=user_id)
    if user_id is None:
        return "No hay Naves favoritas"

    userFavorites = list(map(lambda starships_fav: starships_fav.serialize(), starships_fav))
    return jsonify(userFavorites),201

@app.route('/user/<int:user_id>/favorites/starships/<int:starships_id>', methods=['POST'])
def post_starships_fav(user_id, starships_id):
    favorites = StarshipsFavorites(user_id=user_id, starships_id=starships_id)
    db.session.add(favorites)
    db.session.commit()
    return jsonify(favorites.serialize()), 201

@app.route('/user/<int:user_id>/favorites/starships/<int:starships_id>', methods=['DELETE'])
def delete_starships_fav(user_id, starships_id):
    deleteFav = StarshipsFavorites.query.filter_by(user_id=user_id, starships_id=starships_id).one() #one devuelve el objeto encontrado, sin el one, devuelve el queryobject
    db.session.delete(deleteFav)
    db.session.commit()

    return jsonify(deleteFav.serialize()), 202

###ALL USER FAVORITES###

@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def get_all_user_favorites(user_id):
    people = PeopleFavorites.query.filter_by(user_id=user_id)
    planets = PlanetsFavorites.query.filter_by(user_id=user_id)
    starships = StarshipsFavorites.query.filter_by(user_id=user_id)
    all_people_favorites = list(map(lambda people: people.serialize(), people))
    all_planets_favorites = list(map(lambda planets: planets.serialize(), planets))
    all_starships_favorites = list(map(lambda starships: starships.serialize(), starships))
    return jsonify(all_people_favorites, all_planets_favorites, all_starships_favorites)

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
