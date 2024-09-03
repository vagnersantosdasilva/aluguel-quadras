from flask import  jsonify


def get_all_campo():
    return jsonify({'id': '',
                    'status': 'training.status',
                    'id_dataset': 'training.id_dataset',
                    }), 200


def create_campo(data):
    return jsonify(data),201

def update_campo(data, id):
    return jsonify({'campo':id}),200

def get_campo(id):
    return jsonify({'campo':id}),200

def delete_campo(id):
    return jsonify({'campo':id}),200