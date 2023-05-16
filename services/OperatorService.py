from models.domain.Operator import Operator
from models.entity.OperatorEntity import OperatorEntity
from database.db_session import db_session

class OperatorService:
    def check_user_credentials(self, username, password):
        return True
    
    def operatorExists(self, username):
        return False
    
    def register(self, username, password):
        self.getOperators()
        if(not self.operatorExists(username)):
            print("repositorio.save")

    def getOperators(self):
        try:
            users = db_session.query(OperatorEntity).all()
            for user in users:
                print(user.username)
        except Exception as e:
            print(e)  # Better to use logging in a real-world application
            return False
        

    
