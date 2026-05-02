from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# Initialize app
app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost:5432/binary_apex'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret'

# Initialize database and JWT manager
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Database models
class Detective(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class Suspect(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), nullable=False)

class Case(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

class Interrogation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    suspect_id = db.Column(db.Integer, db.ForeignKey('suspect.id'), nullable=False)
    notes = db.Column(db.Text, nullable=False)

# Endpoints
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')  # Validate this with your user model
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200

@app.route('/detectives', methods=['GET'])
@jwt_required()
def get_detectives():
    detectives = Detective.query.all()
    return jsonify([{'id': d.id, 'name': d.name} for d in detectives])

@app.route('/suspects', methods=['GET'])
@jwt_required()
def get_suspects():
    suspects = Suspect.query.all()
    return jsonify([{'id': s.id, 'name': s.name, 'status': s.status} for s in suspects])

@app.route('/cases', methods=['GET'])
@jwt_required()
def get_cases():
    cases = Case.query.all()
    return jsonify([{'id': c.id, 'title': c.title, 'description': c.description} for c in cases])

@app.route('/interrogations', methods=['GET'])
@jwt_required()
def get_interrogations():
    interrogations = Interrogation.query.all()
    return jsonify([{'id': i.id, 'suspect_id': i.suspect_id, 'notes': i.notes} for i in interrogations])

# Error handler
@app.errorhandler(404)
def not_found(e):
    return jsonify(error='Not found'), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify(error='Internal server error'), 500

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)