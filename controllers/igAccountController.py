# controllers/user_controller.py
from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from services.igAccountService import igAccountService
from models.domain.igAccount import igAccount

class igAccountController:
    operator_service = igAccountService()

    @classmethod
    def register_routes(cls, blueprint):

        @blueprint.route('/registerAccount', methods=['GET', 'POST'])
        def register():
            if request.method == 'POST':
                data = request.get_json()
                username = data['username']
                password = data['password']
                owner = data['owner']
                cls.operator_service.registerAccount(username, password, owner)
                return jsonify({'message': 'OoooK'}), 200

igAccount_blueprint = Blueprint('igAccount', __name__)
igAccountController.register_routes(igAccount_blueprint)