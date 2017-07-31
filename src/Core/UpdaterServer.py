from threading import Thread
import eventlet
import logging


class UpdaterServer(Thread):
    def __init__(self, context):
        Thread.__init__(self)
        self.context = context

    def connect(self, address):
        '''
        Create the server listenner
        '''

        # Create socket Connection and Bind
        self.ssock = eventlet.listen(address)

        logging.info("UpdaterServer : Ready")

    def run(self):
        try:
            while True:
                sock, address = self.ssock.accept()

                logging.info("UpdataerServer - New connection from {}".format(address))

                self.context["updatingConnections"].append(sock)

        except (KeyboardInterrupt, SystemExit):
            print("Server - Exit")
