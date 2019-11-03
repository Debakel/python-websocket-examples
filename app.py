import datetime
import threading
from time import sleep

from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.websocket import WebSocketHandler
from typing import List


class BaseWebSocketHandler(WebSocketHandler):
    def check_origin(self, origin):
        # Allow all origins
        # Otherwise, incoming requests from foreign origins would result in a 403-response.
        return True


class EchoBotHandler(BaseWebSocketHandler):
    """ WebSocketHandler that echoes back all incoming messages to the client.
    """

    def on_message(self, message: str):
        self.write_message('You sent: ' + message)


timebot_handlers: List['TimeBotHandler'] = []


class TimeBotHandler(BaseWebSocketHandler):
    """ WebSocketHandler that sends the current time every 2 seconds to each connected client.
    """

    def open(self, *args, **kwargs):
        timebot_handlers.append(self)

    def close(self, code=None, reason=None):
        timebot_handlers.remove(self)

    def on_message(self, message):
        self.send_time()

    def send_time(self):
        self.write_message("Here's the time: " + datetime.datetime.now().isoformat())


class TimeBotWorkerThread(threading.Thread):
    def run(self):
        while True:
            for handler in timebot_handlers:
                handler.send_time()
            sleep(2)


chat_handlers = []


class ChatHandler(BaseWebSocketHandler):
    """ WebSocketHandler that distributes incoming messages to all other clients connected.
    """

    def open(self, *args, **kwargs):
        chat_handlers.append(self)

    def close(self, code=None, reason=None):
        chat_handlers.remove(self)

    def on_message(self, message):
        for h in chat_handlers:
            if h == self:
                continue
            h.write_message(message)


if __name__ == '__main__':
    app = Application(
        handlers=[
            (r'/echo', EchoBotHandler),
            (r'/time', TimeBotHandler),
            (r'/chat', ChatHandler)
        ]
    )
    app.listen(8001)
    timebot_thread = TimeBotWorkerThread()
    timebot_thread.start()

    IOLoop.current().start()
