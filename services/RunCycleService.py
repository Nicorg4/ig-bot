from models.domain.igAccount import IgAccount
from database.db_session import db_session
from services.igAccountService import IgAccountService
from services.instagram_bot_service import start_bot
from instagram_bot_service import *
import instagram_bot_service

class RunCycleService:
    igAccountService = IgAccountService()

    def runCycle(self, igAccountUsername):
        igAccountEntity = self.igAccountService.getIgPasswordByIgUsername(igAccountUsername)
        instagram_bot_service.IG_USER = igAccountEntity.username
        instagram_bot_service.IG_PASS = igAccountEntity.password
        #start_bot(destinationList, isFirstCycle)
