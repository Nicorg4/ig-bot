# controllers/user_controller.py
from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from services.DestinationParamsService import DestinationParamsService
from models.domain.DestinationParams import DestinationParams

class DestinationParamsController:
    destinationParams_service = DestinationParamsService()

    @classmethod
    def register_routes(cls, blueprint):

        @blueprint.route('/set-params', methods=['GET', 'POST'])
        def register():
            if request.method == 'POST':
                data = request.get_json()
                destinationId = data['destinationId']
                numberOfComments = data['numberOfComments']
                numberOfMessages = data['numberOfMessages']
                cls.destinationParams_service.setDestinationParams(destinationId, numberOfComments, numberOfMessages)
                return jsonify({'message': 'Exito'}), 200
            
        def get():
            if request.method == 'POST':
                data = request.get_json()
                destinationId = data['destinationId']
                cls.destinationParams_service.getDestinationByDestinationId(destinationId)
                return jsonify({'message': 'Exito'}), 200

destinationParams_blueprint = Blueprint('destinationParams', __name__)
DestinationParamsController.register_routes(destinationParams_blueprint)