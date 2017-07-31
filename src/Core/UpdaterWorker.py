
from threading import Thread
import json


class UpdaterWorker(Thread):
    def __init__(self, context):
        Thread.__init__(self)
        self.context = context

    def run(self):
        while True:
            info = self.context["updatingQueue"].get()

            for listennerSock in self.context["updatingConnections"]:
                try:
                    sent = listennerSock.send(str.encode(json.dumps(info)))
                except:
                    self.context["updatingConnections"].remove(listennerSock)
                    listennerSock.close()
