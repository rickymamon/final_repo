from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt, verify_jwt_in_request
from functools import wraps

app = Flask(__name__)
jwt = JWTManager(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:admin@localhost/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'mamonAPIAPP'

db = SQLAlchemy(app)

class Client(db.Model):  
    __tablename__ = 'client'
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(45), nullable=False)
    job_title = db.Column(db.String(45), nullable=False)
    description = db.Column(db.String(45), nullable=False)
    department = db.Column(db.String(45), nullable=False)
    address = db.Column(db.String(45), nullable=False)

def to_dict(self):
        return {
            "id": self.id,
            "fullname": self.fullname,
            "job_title": self.job_title,
            "description": self.description,
            "department": self.department,
            "address": self.address
        }
        
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # Fixed the issue here
    username = data.get('username')
    password = data.get('password')

    if username == 'client' and password == 'clientpass':
        token = create_access_token(identity='client', additional_claims={'role': 'admin'})
        return jsonify({"Access Token" : token}), 200
    else:
        return jsonify({"msg": "Invalid Password or username"}), 401

def role_required(required_role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get('role') != required_role:  # Fixed the comparison here
                return jsonify({"success": False, "msg":"Access forbidden"}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper

@app.route("/clients", methods=["GET"])
@jwt_required()
@role_required('admin')
def get_clients():
    clients = Client.query.all()
    return jsonify(
        {
            "success": True,
            "data": [client.to_dict() for client in clients]
        }
    ), 200
    
@app.route("/clients/<int:id>", methods=['GET'])
@jwt_required()
@role_required('admin')
def get_client(id):
    client = db.session.get(Client, id)
    if not client:
        return jsonify(
            {
                "success": False,
                "error": "Client not found"
            }
        ), 404
    return jsonify(
        {
            "success": True,
            "data": client.to_dict()
        }
    ), 200

@app.route("/clients", methods=['POST'])
@jwt_required()
@role_required('admin')
def add_client():
    if not request.is_json:
        return jsonify(
            {
                "success": False,
                "error": "Content-type must be application/json"
            }
        ), 400

    data = request.get_json()
    required_fields = ["fullname", "job_title", "description", "department", "address"]
    
    for field in required_fields:
        if field not in data:
            return jsonify(
                {
                    "success": False,
                    "error": f"Missing field: {field}"
                }
            ), 400
    
    try:
        new_client = Client(
            fullname=data["fullname"],
            job_title=data["job_title"],
            description=data["description"],
            department=data["department"],
            address=data["address"]
        )
        db.session.add(new_client)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "success": False,
                "error": f"Error adding client: {str(e)}"
            }
        ), 500

