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

    def put(self, params):
        '''
        Perform an operation.
        - reset : Clean a bank
        '''
        try:
            operation = params['operation']
        except:
            raise Exception("operation parameter is required")
        else:
            if operation == "reset":
                return self.client.bank_reset(self.bank)
            else:
                return None
