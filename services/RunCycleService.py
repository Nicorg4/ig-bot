from models.domain.igAccount import IgAccount
from database.db_session import db_session
from services.igAccountService import IgAccountService
from instagram_bot import *
import instagram_bot

class RunCycleService:
    igAccountService = IgAccountService()

    def runCycle(self, igAccountUsername):
        igAccountEntity = self.igAccountService.getIgPasswordByIgUsername(igAccountUsername)
        instagram_bot.IG_USER = igAccountEntity.username
        instagram_bot.IG_PASS = igAccountEntity.password
        #start_bot(destinationList, isFirstCycle)
