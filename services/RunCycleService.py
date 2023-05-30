from models.domain.igAccount import IgAccount
from database.db_session import db_session
from services.igAccountService import IgAccountService
from services.instagram_bot_service import start_bot

class RunCycleService:
    igAccountService = IgAccountService()

    def runCycle(self, igAccountUsername):
        igAccountEntity = self.igAccountService.getIgPasswordByIgUsername(igAccountUsername)
        #start_bot(destinationList, isFirstCycle)
