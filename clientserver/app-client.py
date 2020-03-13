#!/usr/bin/python3

import sys
from libclient import Client

def myargparse(argv):
    """ Parses key value command line arguments into a usable 
        dictionary and list.
        Example:
            ./app-client.py host=10.0.61.34 port=6000 action=search value=rhino whoknows1 whoknows2
        will create:
            kwargs{
                "host":"10.0.61.34",
                "port":"6000",
                "action":"search",
                "value":"rhino"
            }
            args['whoknows1', 'whoknows2']
        and will return them.
    """ 
    kwargs = {}
    args = []

    for arg in argv[1:]:
        if '=' in arg:
            k,v = arg.split("=")
            kwargs[k]=v
        else:
            args.append(arg)
    return (kwargs,args)

if __name__=='__main__':
    kwargs,args = myargparse(sys.argv)
    #print(kwargs,args)

    host = kwargs.get("host",None)
    port = int(kwargs.get("port",None))
    action = kwargs.get("action",None)
    value = kwargs.get("value",None)

    if host and port and action and value:
        client = Client(host,port)
        request = client.create_request(action, value)
