from models.domain.igAccount import igAccount
from models.entity.igAccountEntity import igAccountEntity
from database.db_session import db_session

class igAccountService:

    def registerAccount(self, username, password, owner):
        if(not self.accountExists(username)):
            new_account = igAccountEntity(username=username, password=password, owner=owner)
            db_session.add(new_account)
            db_session.commit()
            print('Cuenta registrada')
        else:
            print('La Cuenta ya existe')

    def accountExists(self, username):
        account_found = db_session.query(igAccountEntity).filter_by(username=username).first()
        if account_found:
            return True
        else:
            return False

    def get_igAccounts(self):
        try:
            accounts = db_session.query(igAccountEntity).all()
            for account in accounts:
                print(account.username)
                print(account.owner)
        except Exception as e:
            print(e)  # Better to use logging in a real-world application
            return False