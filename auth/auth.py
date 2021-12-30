import json

class AuthData:
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret

    @staticmethod
    def CreateFromJson(fileLocation: str) -> 'AuthData': 
        try:
            f = open(fileLocation, 'r')
            data = json.load(f)
            f.close()
        except:
            return None
        consumer_key = data['CONSUMER_KEY']
        consumer_secret = data['CONSUMER_SECRET']
        access_token = data['ACCESS_TOKEN']
        access_token_secret = data['ACCESS_TOKEN_SECRET']
        return AuthData(consumer_key, consumer_secret, access_token, access_token_secret)
    
    def SaveToJson(self, fileLocation: str) -> None:
        dictToDump: dict = {
            "CONSUMER_KEY": self.consumer_key,
            "CONSUMER_SECRET": self.consumer_secret,
            "ACCESS_TOKEN": self.access_token,
            "ACCESS_TOKEN_SECRET": self.access_token_secret
        }
        f = open(fileLocation, "w")
        json.dump(dictToDump, f)
        f.close()