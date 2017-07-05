'''
	Cache API controller
        Part of Multi-thread Cache system
	LICENSE MIT @2017 Ivan Lausuch <ilausuch@gmail.com>
'''


class Cache:
    """
    Cache API
    """

    def __init__(self, client):
        self.client = client

    def getBanks(self):
        '''
        Get all bank names
        '''
        return self.client.bank_list()
