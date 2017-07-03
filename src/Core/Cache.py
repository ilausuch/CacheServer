'''
	Multi-thread Cache system
	LICENSE MIT @2017 Ivan LAusuch <ilausuch@gmail.com>

	CahceItem, CacheBank and Cache
'''

import time
import threading


class CacheItem:
    """
    Cache Item
    """

    def __init__(self, key, value, lifetime=0):
        '''
        Constructor
        '''

        # Some inits
        self.key = key
        self.value = value
        self.lifetime = lifetime

        # Start timeout
        self.resetTimeout()

    def checkTimeout(self):
        '''
        Check timeout
        '''
        if self.timeout == 0:
            return True
        else:
            return self.timeout > time.time()

    def resetTimeout(self):
        '''
        Reset timeout
        '''
        # Calcule timeout when it will die
        if self.lifetime == 0:
            self.timeout = 0
        else:
            self.timeout = time.time() + self.lifetime


class CacheBank:
    """
    Cache Bank
    """

    def __init__(self, name):
        '''
        Constructor
        '''
        self.name = name

        # Init dictionary
        self.dictionary = {}

        # Create a lock for each bank
        self.lock = threading.RLock()

    def put(self, item):
        '''
        Put a new element in this bank.
        '''

        # Adquire the lock to protect this code
        self.lock.acquire()

        # Put the new item into the dictionary
        self.dictionary[item.key] = item

        # Release the lock
        self.lock.release()

    def get(self, key):
        '''
        Get an element from this bank
        '''

        # Adquire the lock to protect folowing code
        self.lock.acquire()

        try:
            # Get the item from the dictionary
            item = self.dictionary[key]

            result = True

        except:
            # Return none if i wasn't found
            item = None

            result = False

        else:
            # Check if this item is alive yet
            if not item.checkTimeout():
                # If isn't alive delete it from the bank
                self.delete(key)

                # Return none in this case
                item = None

                # Will generate an exception
                result = False
            else:

                # Will return the item
                result = True

        finally:
            # Release the lock
            self.lock.release()

        if not result:
            raise(Exception("Key {} doesn't exist".format(key)))
        else:
            return item

    def touch(self, key):
        '''
        Get an element from this bank
        '''

        # Adquire the lock to protect folowing code
        self.lock.acquire()

        try:
            # Get the item from the dictionary
            item = self.dictionary[key]

            # Will return the item
            result = True

        except:
            # Will generate an exception
            result = False

        else:
            # Check if this item is alive yet
            if not item.checkTimeout():
                # If isn't alive delete it from the bank
                self.delete(key)

                # Return none in this case
                item = None

                # Will generate an exception
                result = False
            else:
                # Reset timeout
                item.resetTimeout()

                # Will return the item
                result = True

        finally:
            # Release the lock
            self.lock.release()

        if not result:
            raise(Exception("Key {} doesn't exist".format(key)))
        else:
            return item

    def delete(self, key):
        '''
        Delete an entry
        '''
        # Adquire the lock to protect folowing code
        self.lock.acquire()

        try:
            # Remove the item from the dictionary
            del self.dictionary[key]

        except:
            # Will generate an exception
            result = False

        else:
            # Will return the item
            result = True

        finally:
            # Release the lock
            self.lock.release()

        if not result:
            raise(Exception("Key {} doesn't exist".format(key)))

    def reset(self):
        '''
        Remove all elemnts of the bank
        '''
        # Adquire the lock to protect folowing code
        self.lock.acquire()

        # Set a new dictionary
        self.dictionary = {}

        # Release the lock
        self.lock.release()

    def update(self):
        '''
        Check the expiration of all elements of the bank
        '''
        # Adquire the lock to protect folowing code
        self.lock.acquire()

        # Prepare and empty list of elements to remove
        listToRemove = []

        # Extract the list of elements to remove
        for key in self.dictionary:
            if not self.dictionary[key].checkTimeout():
                listToRemove.append(key)

        # Remove all these elements
        for key in listToRemove:
            self.dictionary[key] = None

        # Release the lock
        self.lock.release()

    def keys(self):
        '''
        Get the list of keys
        '''

        # Update all elements of the bank
        self.update()

        # Adquire the lock to protect folowing code
        self.lock.acquire()

        # Return the dictionary keys
        keys = list(self.dictionary.keys())

        # Release the lock
        self.lock.release()

        return keys


class Cache:
    """
    Cache library
    """

    def __init__(self):
        # Init bank dictionary
        self.banks = {}

        # Create a lock for bank manipulation
        self.lock = threading.RLock()

    def getBank(self, name):
        '''
        Gets a bank or creates it
        '''

        # Adquire the lock to protect folowing code
        self.lock.acquire()

        try:
            # Get a bank
            bank = self.banks[name]
        except:
            # If doesn't exist create a new one
            bank = CacheBank(name)

            # Put the new bank in the dictionary
            self.banks[name] = bank

        # Release the lock
        self.lock.release()

        # Return the selected bank
        return bank

    def getBanks(self):

                # Adquire the lock to protect folowing code
        self.lock.acquire()

        # Get the keys
        keys = list(self.banks.keys())

        # Release the lock
        self.lock.release()

        # Return the list of key names
        return keys

    def get(self, bankName, key):
        # Get a item from a bank
        return self.getBank(bankName).get(key)

    def put(self, bankName, item):
        # Put a intem into a bank
        self.getBank(bankName).put(item)

    def touch(self, bankName, item):
        self.getBank(bankName).touch(item)

    def delete(self, bankName, item):
        self.getBank(bankName).delete(item)
