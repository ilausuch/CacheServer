'''
	Bank API controller
        Part of Multi-thread Cache system
	LICENSE MIT @2017 Ivan Lausuch <ilausuch@gmail.com>
'''
class Bank:
    """
    Bank API
    """
    def __init__(self, client, bank):
        self.client = client
        self.bank = bank
        
    def getKeys(self):
        '''
        Get all key entities of a bank
        '''
        return self.client.bank_keys(self.bank)
    
    def put(self, request):
        '''
        Perform an operation.
        - reset : Clean a bank
        '''
        operation = request.args.get('operation')
        
        if operation == None:
            raise Exception("operation parameter is required")
        
        elif operation == "reset":
            return self.client.bank_reset(self.bank)
        
        else:
            raise Exception("Unkown operation %s" % operation)
      