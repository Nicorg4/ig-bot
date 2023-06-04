from models.domain.Operator import Operator
from models.entity.OperatorEntity import OperatorEntity
from database.db_session import db_session

class OperatorService:
    def check_user_credentials(self, username, password):
        return db_session.query(OperatorEntity).filter_by(username=username, password=password).first()

    
    def operatorExists(self, username):
        return db_session.query(OperatorEntity).filter_by(username=username).first()

    
    def register(self, username, password):
        if(not self.operatorExists(username)):
            new_operator = OperatorEntity(username=username, password=password)
            db_session.add(new_operator)
            db_session.commit()
            print('Usuario registrado')
        else:
            print('El usuario ya existe')

    def login(self, username, password):
        if self.check_user_credentials(username, password):
            return True 
        else:
           return False

    def getOperators(self):
        try:
            users = db_session.query(OperatorEntity).all()
            for user in users:
                print(user.username)
        except Exception as e:
            print(e)  # Better to use logging in a real-world application
            return False
        

    
