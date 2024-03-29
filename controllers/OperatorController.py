# controllers/user_controller.py
from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from services.OperatorService import OperatorService
from models.domain.Operator import Operator

class OperatorController:
    operator_service = OperatorService()

    @classmethod
    def register_routes(cls, blueprint):
        @blueprint.route('/login', methods=['GET', 'POST'])
        def login():
            data = request.get_json()
            username = data['username']
            password = data['password']
            
            success = cls.operator_service.login(username, password)
            if success:
                return jsonify({'message': 'Success'}), 200
            else:
                return jsonify({'message': 'Invalid credentials'}), 401

        @blueprint.route('/register', methods=['GET', 'POST'])
        def register():
            if request.method == 'POST':
                data = request.get_json()
                username = data['username']
                password = data['password']
                cls.operator_service.register(username, password)
                return jsonify({'message': 'Exito'}), 200
            
        @blueprint.route('/get-operators', methods=['GET', 'POST'])
        def get():
            if request.method == 'GET':
                cls.operator_service.getOperators()
                return jsonify({'message': 'Exito'}), 200

operator_blueprint = Blueprint('operator_blueprint', __name__)
OperatorController.register_routes(operator_blueprint)