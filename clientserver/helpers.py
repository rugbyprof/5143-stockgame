import sys

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
