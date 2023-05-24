from models.domain.Cycle import Cycle
from models.entity.CycleEntity import CycleEntity
from database.db_session import db_session

class CycleService:

    def createCycle(self, destList):
        new_cycle = CycleEntity(destinationParamsList=destList)
        # db_session.add(new_destinationParams)
        # db_session.commit()
        print('Ciclo creado: ', new_cycle.destinationParamsList)