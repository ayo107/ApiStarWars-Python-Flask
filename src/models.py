from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    uid = db.Column(db.Integer, unique=True)
    height = db.Column(db.Integer())
    mass = db.Column(db.Integer())
    hair_color = db.Column(db.String(250))
    homeworld = db.Column(db.String(250))
    eye_color = db.Column(db.String(250))
    gender = db.Column(db.String(250)) 
    favorites = db.relationship('PeopleFavorites', backref='people', lazy=True)

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "uid": self.uid,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "homeworld": self.homeworld,
            "eye_color": self.eye_color,
            "gender": self.gender
            # do not serialize the password, its a securi
        }

class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    uid = db.Column(db.Integer, unique=True)
    diameter = db.Column(db.Integer())
    population = db.Column(db.Integer())
    climate = db.Column(db.String(250))
    terrain = db.Column(db.String(250))
    surface_water = db.Column(db.Integer())
    favorites = db.relationship('PlanetsFavorites', backref='planets', lazy=True)

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "uid": self.uid,
            "diameter": self.diameter,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water
            # do not serialize the password, its a security breach
        }

class Starships(db.Model):
    __tablename__ = "starships"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable = False)
    uid = db.Column(db.Integer, unique=True)
    model = db.Column(db.String(250))
    cost = db.Column(db.Integer())
    passengers = db.Column(db.Integer())
    cargo_capacity = db.Column(db.Integer())
    favorites = db.relationship('StarshipsFavorites', backref='starships', lazy=True)

    def __repr__(self):
        return '<Starships %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "uid": self.uid,
            "model": self.model,
            "cost": self.cost,
            "passengers": self.passengers,
            "cargo_capacity": self.cargo_capacity
        }
   
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)
    favorites = db.relationship('PeopleFavorites', backref='user', lazy=True)
    favorites2 = db.relationship('PlanetsFavorites', backref='user', lazy=True)
    favorites3 = db.relationship('StarshipsFavorites', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            # do not serialize the password, its a security breach
        }

class PeopleFavorites(db.Model):
    __tablename__ = 'peoplefavorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'))
    favorites = db.relationship('Favorites', backref='peoplefavorites', lazy=True)

    def __repr__(self):
        return 'PeopleFavorites %r>' % self.user_id
    
    def serialize(self):
        return {
            'user_id': self.user_id,
            'people_id': self.people_id
        }

class PlanetsFavorites(db.Model):
    __tablename__ = 'planetsfavorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    planets_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    favorites = db.relationship('Favorites', backref='planetsfavorites', lazy=True)

    def __repr__(self):
        return 'PlanetsFavorites %r>' % self.user_id
    
    def serialize(self):
        return {
            'user_id': self.user_id,
            'planets_id': self.planets_id
        }

class StarshipsFavorites(db.Model):
    __tablename__ = 'starshipsfavorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    starships_id = db.Column(db.Integer, db.ForeignKey('starships.id'))
    favorites = db.relationship('Favorites', backref='starshipsfavorites', lazy=True)

    def __repr__(self):
        return 'StarshipsFavorites %r>' % self.user_id
    
    def serialize(self):
        return {
            'user_id': self.user_id,
            'starships_id': self.starships_id
        }

class Favorites(db.Model):
    __tablename__= 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    people_id = db.Column(db.Integer, db.ForeignKey('peoplefavorites.id'))
    planets_id = db.Column(db.Integer, db.ForeignKey('planetsfavorites.id'))
    starships_id = db.Column(db.Integer, db.ForeignKey('starshipsfavorites.id'))

    def __repr__(self):
        return 'PeopleFavorites %r>' % self.user_id
    
    def serialize(self):
        return {
            'user_id': self.user_id,
            'people_id': self.people_id,
            'planets_id': self.planets_id,
            'starships_id': self.starships_id
        }