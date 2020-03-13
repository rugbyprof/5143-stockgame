
def logg(message):
    f = open("logfile.log","a")
    f.write(message+"\n")
    f.close()


class DataBase(object):
    """
    constructor
    """
    def __init__(self,request):
        self.request = request
        self.action = self.request["action"]

        self.fakeDB = {
            "morpheus": "Follow the white rabbit. \U0001f430",
            "ring": "In the caves beneath the Misty Mountains. \U0001f48d",
            "dogface": "\U0001f43e Playing ball! \U0001f3d0",
            "gorilla":"\U0001F98D",
            "dog":"\U0001F415",
            "camel":"\U0001F42A",
            "rhino":"\U0001F98F"
        }

    def processRequest(self):
        if self.action == "search":
            query = self.request.get("key")
            answer = self.search(query)
            content = {"result": answer}
        elif action == "insert":
            collection = self.request.get("collection")
            data = self.request.get("data")
            answer = self.insert(collection,data)
            content = {"result": answer}
        else:
            content = {"result": f'Error: invalid action "{action}".'}

    def search(self,key=None):
        if not key:
            logg("key = none")
            return {"error":"key is none"}
        if key in self.fakeDB:
            value = self.fakeDB[key]
            return {"response":value}
        else:
            return {"response":{"error":f"Key: {key} not found"}}

        
    
    def insert(self,collection=None,data=None):
        if not collection:
            response = {"Error": "collection = None"}
        elif not data:
            response = {"Error": "data = None"}

        response = {"success": {"message": {"insert":f"inserting into {collection}","data":data}}}
