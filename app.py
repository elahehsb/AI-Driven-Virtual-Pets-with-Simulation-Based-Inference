from flask import Flask, request, jsonify
from pet_simulator import VirtualPet
import json

app = Flask(__name__)
pet = VirtualPet()

@app.route('/interact', methods=['POST'])
def interact():
    action = request.json.get('action')
    pet.interact(action)
    pet.update_state()
    return jsonify(pet.get_state())

@app.route('/state', methods=['GET'])
def get_state():
    return jsonify(pet.get_state())

if __name__ == '__main__':
    app.run(debug=True)
