from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from sqlalchemy import Column, Integer, String, Float, create_engine, MetaData
from sqlalchemy.orm import create_session
from sqlalchemy.ext.declarative import declarative_base
from flask_marshmallow import Marshmallow

# Create an engine for connecting to SQLite3.
e = create_engine('sqlite:///CPDB.db')
Base = declarative_base(e)
metadata = MetaData(bind=e)

# flask app initialisation
app = Flask(__name__)
api = Api(app)

# marshmallow initialisation
ma = Marshmallow(app)


# create a model from an existsing relation in the DB
class ChordProgression(Base):
    __tablename__ = 'chord_progressions'
    chord_HTML = Column(String)
    child_path = Column(String, primary_key=True)
    valence = Column(Float)
    energy = Column(Float)


# marshmallow output format
class ChordProgressionSchema(ma.Schema):
    class Meta:

        # fields to expose
        fields = ("chord_HTML", "child_path", "valence", "energy")


# home page with information about the endpoints
class HomePage(Resource):
    def get(self):

        # detail the endpoints
        endpoints = {'endpoints': [{'endpoint': '/api/all', 'info': 'Get all the available chord progressions in the database.'}, {
            'endpoint': '/api/filter', 'info': 'Filter chord progressions based on valence and energy values. Request format: /api/filter?valence=0.4&energy=0.6'}, ]}

        return jsonify(endpoints)


# get all chords in the DB
class AllChordProgressions(Resource):
    def get(self):

        # schema initialisation
        chord_progression_schema = ChordProgressionSchema(many=True)

        # connect to database
        session = create_session(bind=e)

        # query DB and return results using the marshmallow schema
        allChordProgressions = session.query(ChordProgression).all()
        return chord_progression_schema.dump(allChordProgressions)


# get chords with specific valence and energy filters
class FilteredChordProgressions(Resource):
    def get(self):

        # schema initialisation
        chord_progression_schema = ChordProgressionSchema(many=True)

        # connect to database
        session = create_session(bind=e)

        # parse valence and energy arguments
        valence = float(request.args.get('valence'))
        energy = float(request.args.get('energy'))

        # query DB using filters and return results using the marshmallow schema
        # +- 0.05 is used for approximation
        filteredChordProgressions = session.query(
            ChordProgression).filter(
                ChordProgression.valence < valence + 0.05,
                ChordProgression.valence > valence - 0.05,
                ChordProgression.energy < energy + 0.05,
                ChordProgression.energy > energy - 0.05
        )
        return chord_progression_schema.dump(filteredChordProgressions)


# define endpoints
api.add_resource(HomePage, '/')
api.add_resource(AllChordProgressions, '/api/all')
api.add_resource(FilteredChordProgressions, '/api/filter')

if __name__ == '__main__':
    app.run(debug=True)
