
def logg(message):
    f = open("logfile.log","a")
    f.write(message+"\n")
    f.close()

class DataBase(object):
    """
    constructor
    """
    def __init__(self):
        self.fakeDB = {
            "morpheus": "Follow the white rabbit. \U0001f430",
            "ring": "In the caves beneath the Misty Mountains. \U0001f48d",
            "dogface": "\U0001f43e Playing ball! \U0001f3d0",
            "gorilla":"\U0001F98D",
            "dog":"\U0001F415",
            "camel":"\U0001F42A",
            "rhino":"\U0001F98F"
        }

    def search(self,key):
        if not key:
            logg("key = none")
            return {"error":"key is none"}
        if key in self.fakeDB:
            value = self.fakeDB[key]
            return {"response":value}
        else:
            return {"response":{"error":f"Key: {key} not found"}}

        
    
    def insert(self,collection,data):
        # print(f"inserting into {collection}")
        # print(data)
        return {"inserting": f"inserting into {collection}","data":data}
