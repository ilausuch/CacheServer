
class Entity:
    """
    Entity API
    """
    def __init__(self, client, bank, key):
        self.client = client
        self.bank = bank
        self.key = key
        
    def get(self):
        return self.client.entity_get(self.bank,self.key)
    
    def post(self, data):
        return self.client.entity_put(self.bank,self.key,data)
    
    def put(self, request):
        operation = request.args.get('operation')
        
        if operation == None:
            raise Exception("operation parameter is required")
        
        elif operation == "touch":
            return self.client.entity_touch(self.bank,self.key)
        
        else:
            raise Exception("Unkown operation %s" % operation)
