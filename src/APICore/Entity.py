'''
	Entity API controller
        Part of Multi-thread Cache system
	LICENSE MIT @2017 Ivan Lausuch <ilausuch@gmail.com>
'''


class Entity:
    """
    Entity API
    """

    def __init__(self, client, bank, key):
        self.client = client
        self.bank = bank
        self.key = key

    def get(self):
        '''
        Get a entry of a bank
        '''
        return self.client.entry_get(self.bank, self.key)

    def post(self, data):
        '''
        Insert or replace a entry of a bank
        '''
        return self.client.entry_set(self.bank, self.key, data)

    def put(self, params):
        '''
        Perform an operation
        - touch: Update lifetime of the entry
        '''
        try:
            operation = params["operation"]
        except:
            raise Exception("operation parameter is required")
        else:
            if operation == "touch":
                return self.client.entry_touch(self.bank, self.key)

            elif operation == "incr":
                try:
                    value = params['value']
                except:
                    raise Exception("value parameter is required")
                else:
                    if value is None:
                        raise Exception("operation parameter is required")

                    try:
                        fvalue = float(value)
                    except:
                        raise Exception("operation parameter is required")
                    else:
                        return self.client.entry_incr(self.bank, self.key, fvalue)

            else:
                raise Exception("Unkown operation %s" % operation)
