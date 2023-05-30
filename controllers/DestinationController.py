# controllers/user_controller.py
from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from services.DestinationService import DestinationService
from models.domain.Destination import Destination

class DestinationController:
    destination_service = DestinationService()

    @classmethod
    def register_routes(cls, blueprint):
        @blueprint.route('/register-destination', methods=['GET', 'POST'])
        def register():
            if request.method == 'POST':
                data = request.get_json()
                locationId = data['locationId']
                locationName = data['locationName']
                placeName = data['placeName']
                hashtag = data['hashtag']
                type = data['type']
                cls.destination_service.registerDestination(locationId, locationName, placeName, hashtag, type)
                return jsonify({'message': 'Exito'}), 200
            
        @blueprint.route('/get-destinations', methods=['GET', 'POST'])
        def get():
            if request.method == 'GET':
                try:
                    destinations = cls.destination_service.getDestinations()
                    # Assuming your DestinationEntity has a method to convert it to dict
                    destinations_json = [destination.to_dict() for destination in destinations]
                    return jsonify({'destinations': destinations_json}), 200
                except Exception as e:
                    return jsonify({'error': str(e)}), 500



destination_blueprint = Blueprint('destination_blueprint', __name__)
DestinationController.register_routes(destination_blueprint)