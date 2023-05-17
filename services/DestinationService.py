from models.domain.Destination import Destination
from models.entity.DestinationEntity import DestinationEntity
from database.db_session import db_session

class DestinationService:    
    def registerDestination(self, locationId, locationName, placeName, hashtag):
        if(not self.destinationExists(locationId, placeName, hashtag)):
            new_destination = DestinationEntity(locationId=locationId, locationName=locationName, placeName=placeName, hashtag=hashtag)
            db_session.add(new_destination)
            db_session.commit()
            print('Destino registrado')
        else:
            print('El Destino ya existe')

    def destinationExists(self, locationId, placeName, hashtag):
        if self.checkLocationIdExists(locationId) or self.checkPlaceNameExists(placeName) or self.checkHashtagExists(hashtag):
            return True
        else:
            return False

    def checkLocationIdExists(self, locationId):
        if locationId == '':
            return False
        locationIdFound = db_session.query(DestinationEntity).filter_by(locationId=locationId).first()
        if locationIdFound:
            return True
        return False
        
    def checkPlaceNameExists(self, placeName):
        if placeName == '':
            return False
        placeNameFound = db_session.query(DestinationEntity).filter_by(placeName=placeName).first()
        if placeNameFound:
            return True
        return False
        
    def checkHashtagExists(self, hashtag):
        if hashtag == '':
            return False
        hashtagFound = db_session.query(DestinationEntity).filter_by(hashtag=hashtag).first()
        if hashtagFound:
            return True
        return False
        
    def getDestinations(self):
        try:
            destinations = db_session.query(DestinationEntity).all()
            for destination in destinations:
                print(destination)
        except Exception as e:
            print(e)  # Better to use logging in a real-world application
            return False
        

    
