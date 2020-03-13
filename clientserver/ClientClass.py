import sys
import selectors
import json
import io
import struct
import socket
import traceback

from Message import ClientMessage

class Request:
    def __init__(self):
        self.request = {}
        self.request["type"] = "text/json"
        self.request["encoding"] = "utf-8"
        self.request['content'] = {}

    def searchRequest(self, key):
        self.request["content"]["action"] = "search"
        self.request["content"]["key"] = key

        return self.request

    def insertRequest(self, collection, data):
        self.request["content"]["action"] = "insert"
        self.request["content"]["collection"] = collection
        self.request["content"]["data"] = data

        return self.request

    def catchAllRequest(self,kwargs):
        self.request["content"]["Error"] = True
        for k,v in kwargs.items():
            self.request["content"][k] = v

        return self.request

    def createRequest(self, **kwargs):

        # Pull all the possible vars out of kwargs
        action = kwargs.get("action", None)
        key = kwargs.get("key", None)
        collection = kwargs.get("collection", None)
        data = kwargs.get("data", None)
        value = kwargs.get("value", None)

        if action == "search":
            request = self.searchRequest(key)
        elif action == "insert":
            request = self.insertRequest(value, data)
        else:
            request = self.catchAllRequest(kwargs)

        return request


class Client:
    def __init__(self, host, port,debug=False):
        self.sel = selectors.DefaultSelector()
        self.host = host
        self.port = port
        self.debug = debug
        self.response = None

    def start_connection(self, request):
        addr = (self.host, self.port)
        if self.debug:
            print("starting connection to", addr)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        message = ClientMessage(self.sel, sock, addr, request)
        self.sel.register(sock, events, data=message)

        try:
            while True:
                events = self.sel.select(timeout=1)
                for key, mask in events:
                    message = key.data
                    try:
                        message.process_events(mask)
                    except Exception:
                        print(
                            "main: error: exception for",
                            f"{message.addr}:\n{traceback.format_exc()}",
                        )
                        message.close()
                # Check for a socket being monitored to continue.
                if not self.sel.get_map():
                    break
        except KeyboardInterrupt:
            print("caught keyboard interrupt, exiting")
        finally:
            self.sel.close()
            self.response = message.response

    def get_response(self):
        return self.response
