from models.domain.DestinationParams import DestinationParams
from models.entity.DestinationParamsEntity import DestinationParamsEntity
from database.db_session import db_session

class DestinationParamsService:

    def setDestinationParams(self, id, comments, messages):
        new_destinationParams = DestinationParamsEntity(destinationId=id, numberOfMessages=comments, numberOfComments=messages)
        # db_session.add(new_destinationParams)
        # db_session.commit()
        print('Parametros creados: ', new_destinationParams.destinationId, new_destinationParams.numberOfMessages, new_destinationParams.numberOfComments)

    def getDestinationByDestinationId(self, id):
        destinationParams = db_session.query(DestinationParamsEntity).filter_by(destinationId=id).first()
        locationName = destinationParams.destinationId_obj.locationName
        placeName = destinationParams.destinationId_obj.placeName
        hashtag = destinationParams.destinationId_obj.hashtag
        
        if placeName != '':
            print(placeName)
        elif hashtag != '':
            print(hashtag)
        else:
            print(locationName)