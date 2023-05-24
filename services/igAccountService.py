from models.domain.IgAccount import IgAccount
from models.entity.IgAccountEntity import IgAccountEntity
from database.db_session import db_session

class IgAccountService:

    def registerAccount(self, username, password, owner):
        if(not self.accountExists(username)):
            new_account = IgAccountEntity(username=username, password=password, owner=owner)
            db_session.add(new_account)
            db_session.commit()
            print('Cuenta registrada')
        else:
            print('La Cuenta ya existe')

    def accountExists(self, username):
        return db_session.query(IgAccountEntity).filter_by(username=username).first()

    def getIgAccounts(self):
        try:
            accounts = db_session.query(IgAccountEntity).all()
            print(accounts)
            for account in accounts:
                print(account.username)
                print(account.owner)
        except Exception as e:
            print(e)  # Better to use logging in a real-world application
            return False
        
    def getOwnerByIgUsername(self, igUsername):
        if(not self.accountExists(igUsername)):
            print('No existe la cuenta')
            return False
        else:
            account = db_session.query(IgAccountEntity).filter_by(username=igUsername).first()
            print(account.owner_obj.username)
            return True