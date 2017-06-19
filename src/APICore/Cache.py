  
class Cache:
    """
    Cache API
    """
    def __init__(self,client):
        self.client = client
    
    def getBanks(self):
        return self.client.bank_list()
    