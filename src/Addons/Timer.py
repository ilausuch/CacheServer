import datetime

class Timer:
    
    def __init__(self):
        self.start()
    
    def start(self):
        self.t1=datetime.datetime.utcnow()
        
    def end(self):
        self.t2=datetime.datetime.utcnow()
        return ((self.t2-self.t1).seconds+(self.t2-self.t1).microseconds/1e6)