import sys
import socket 
import ifcfg
import json
import pprint


# Function to display hostname and 
# IP address 
def get_Host_name_IP(): 
    try: 
        host_name = socket.gethostname() 
        host_ip = socket.gethostbyname(host_name) 
        print("Hostname :  ",host_name) 
        print("IP : ",host_ip) 
    except: 
        print("Unable to get Hostname and IP") 

def get_IP():
    ip = None
    result = ifcfg.interfaces()
    
    for k,v in result.items():
        if v['inet'] != None and v['inet'] != '127.0.0.1':
            return v['inet']
    return ip


        

def myArgParse(argv):
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
    # Driver code 
   
    print(get_IP())