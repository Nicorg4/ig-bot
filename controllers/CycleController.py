# controllers/user_controller.py
from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from services.CycleService import CycleService
from models.domain.Cycle import Cycle

class DestinationParamsController:
    cycle_service = CycleService()

    @classmethod
    def register_routes(cls, blueprint):
        @blueprint.route('/create-cycle', methods=['GET', 'POST'])
        def register():
            if request.method == 'POST':
                data = request.get_json()
                destinationParamsList = data['destinationParamsList']
                cls.cycle_service.createCycle(destinationParamsList)
                return jsonify({'message': 'Exito'}), 200
            
        @blueprint.route('/get-cycles', methods=['GET', 'POST'])
        def get():
            if request.method == 'GET':
                cls.cycle_service.getCycles()
                return jsonify({'message': 'Exito'}), 200

cycle_blueprint = Blueprint('cycle', __name__)
DestinationParamsController.register_routes(cycle_blueprint)