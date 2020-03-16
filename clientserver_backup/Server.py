""" Server.py
Look at above shebang and make sure your python is at same location.
You can test by typing `which python3` at your console.

Description:
    Listens at indicated ip address and port for incoming requests.
Requires:
    ServerClass.py
Usage:
    Configure server using key value pairs: 
    ./Server.py host=10.0.61.34 port=6000
"""

import sys
from helpers import myArgParse
from ServerClass import Server


def Usage():
    print("Usage: <host> <port>")
    print(f"Example: {sys.argv[0]} host=10.0.61.34 port=6000")
    sys.exit()

if __name__=='__main__':
    """ Server driver. It uses libserver.py to start listening <host> <port>
        Requires:
            libserver.py
        Usage:
            Pass in values to the client using key value pairs 
            ./app-server.py host=10.0.61.34 port=6000 
    """
    kwargs,args = myArgParse(sys.argv)
    #print(kwargs,args)

    host = kwargs.get("host",None)
    port = int(kwargs.get("port",None))

    if not (host and port):
        Usage()

    server = Server(host,port)
    server.run_server()

 
