from models.domain.Operator import Operator
from models.entity.OperatorEntity import OperatorEntity
from database.db_session import db_session

class OperatorService:
    def check_user_credentials(self, username, password):
        user_found = db_session.query(OperatorEntity).filter_by(username=username, password=password).first()
        if user_found:
            return True
        else:
            return False
    
    def operatorExists(self, username):
        user_found = db_session.query(OperatorEntity).filter_by(username=username).first()
        if user_found:
            return True
        else:
            return False
    
    def register(self, username, password, ranking):
        if(not self.operatorExists(username)):
            new_operator = OperatorEntity(username=username, password=password, ranking=ranking)
            db_session.add(new_operator)
            db_session.commit()
            print('Usuario registrado')
        else:
            print('El usuario ya existe')

    def login(self, username, password):
        if self.check_user_credentials(username, password):
            print('Usuario loggeado')
        else:
            print('Credenciales incorrectas')

    def getOperators(self):
        try:
            users = db_session.query(OperatorEntity).all()
            for user in users:
                print(user.username)
        except Exception as e:
            print(e)  # Better to use logging in a real-world application
            return False
        

    
