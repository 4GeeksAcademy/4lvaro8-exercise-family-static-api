"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_members():
    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    return jsonify(members), 200


@app.route('/member/<int:id>', methods=['GET'])
def get_one_member(id):
    member = jackson_family.get_member(id)
    print("El miembro de la familia es", member)
    if member is None:
        return jsonify({"msg": "no se encontró ningún miembro"}), 404
    return jsonify(member), 200
  


@app.route('/member', methods=['POST'])
def add_member():
    new_member = request.json
    print(new_member)
    if new_member:
        jackson_family.add_member(new_member)
        return  ({"msg": "Un nueo miembro ha sido añadido"}), 200
    return ({"error": "Invalid request"}), 400


@app.route('/member/<int:id>', methods=['DELETE'])
def delete_members(id):
    response = jackson_family.delete_member(id)
    if response is None:
        return jsonify({"msg": "no se encontró ningún miembro"}), 404
    elif response:
        return jsonify(response), 200
    else:
        return ({"error": "Invalid request"}), 400


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
