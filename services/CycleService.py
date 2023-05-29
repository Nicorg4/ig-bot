from models.domain.Cycle import Cycle
from models.entity.CycleEntity import CycleEntity
from database.db_session import db_session

class CycleService:

    def createCycle(self, destList):
        new_cycle = CycleEntity(destinationParamsList=destList)
        db_session.add(new_cycle)
        db_session.commit()
        print('Ciclo creado: ', new_cycle.destinationParamsList)

    def getCycles(self):
        cycles = db_session.query(CycleEntity)

        for cycle in cycles:
            print(cycle)