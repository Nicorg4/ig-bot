# controllers/user_controller.py
from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from services.CycleService import CycleService
from models.domain.Cycle import Cycle
from services.RunCycleService import RunCycleService

class DestinationParamsController:
    runCycleService = RunCycleService()

    @classmethod
    def register_routes(cls, blueprint):
        @blueprint.route('/run-cycle', methods=['GET', 'POST'])
        def runBot():
            if request.method == 'POST':
                data = request.get_json()
                cls.runCycleService.runCycle("igusername2")
                return jsonify({'message': 'Exito'}), 200
            

bot_blueprint = Blueprint('bot', __name__)
DestinationParamsController.register_routes(bot_blueprint)