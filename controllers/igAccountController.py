# controllers/user_controller.py
from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from services.igAccountService import IgAccountService
from models.domain.igAccount import IgAccount

class IgAccountController:
    igAccount_service = IgAccountService()

    @classmethod
    def register_routes(cls, blueprint):

        @blueprint.route('/register-account', methods=['GET', 'POST'])
        def register():
            if request.method == 'POST':
                data = request.get_json()
                username = data['username']
                password = data['password']
                owner = data['owner']
                cls.igAccount_service.registerAccount(username, password, owner)
                return jsonify({'message': 'Exito'}), 200
            
        @blueprint.route('/get-accounts', methods=['GET', 'POST'])
        def getAccounts():
            if request.method == 'GET':
                cls.igAccount_service.getIgAccounts()
                return jsonify({'message': 'Exito'}), 200
            
        @blueprint.route('/get-owner', methods=['GET', 'POST'])
        def getOwner():
            if request.method == 'GET':
                data = request.get_json()
                accountUsername = data['username']
                cls.igAccount_service.getOwnerByIgUsername(accountUsername)
                return jsonify({'message': 'Exito'}), 200

igAccount_blueprint = Blueprint('igAccount', __name__)
IgAccountController.register_routes(igAccount_blueprint)