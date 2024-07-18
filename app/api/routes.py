from flask import Blueprint, request, jsonify
from helpers import token_required
from models import db, Monster, monster_schema, monsters_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/monsters', methods=['POST'])
@token_required
def create_monster(current_user_token):
    try:
        name = request.json['name']
        height = request.json['height']
        weight = request.json['weight']
        specialty = request.json['specialty']
        type = request.json['type']
        power_level = request.json['power_level']
        user_token = current_user_token.token

        monster = Monster(
            name=name,
            height=height,
            weight=weight,
            specialty=specialty,
            type=type,
            power_level=power_level,
            user_token=user_token
        )

        db.session.add(monster)
        db.session.commit()

        response = monster_schema.dump(monster)
        return jsonify(response), 201  # 201 Created status for successful creation
    except KeyError as e:
        return jsonify({'error': f'Missing required field: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/monsters', methods=['GET'])
@token_required
def get_monsters(current_user_token):
    try:
        a_user = current_user_token.token
        monsters = Monster.query.filter_by(user_token=a_user).all()
        response = monsters_schema.dump(monsters)
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/monsters/<id>', methods=['GET'])
@token_required
def get_individual_monster(current_user_token, id):
    try:
        monster = Monster.query.get(id)
        if not monster:
            return jsonify({'error': 'Monster not found'}), 404
        response = monster_schema.dump(monster)
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/monsters/<id>', methods=['PUT'])
@token_required
def update_monster(current_user_token, id):
    try:
        monster = Monster.query.get(id)
        if not monster:
            return jsonify({'error': 'Monster not found'}), 404

        # Update fields from request JSON
        monster.name = request.json.get('name', monster.name)
        monster.height = request.json.get('height', monster.height)
        monster.weight = request.json.get('weight', monster.weight)
        monster.specialty = request.json.get('specialty', monster.specialty)
        monster.type = request.json.get('type', monster.type)
        monster.power_level = request.json.get('power_level', monster.power_level)
        monster.user_token = current_user_token.token

        db.session.commit()
        response = monster_schema.dump(monster)
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/monsters/<id>', methods=['DELETE'])
@token_required
def delete_monster(current_user_token, id):
    try:
        monster = Monster.query.get(id)
        if not monster:
            return jsonify({'error': 'Monster not found'}), 404

        db.session.delete(monster)
        db.session.commit()
        response = monster_schema.dump(monster)
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500