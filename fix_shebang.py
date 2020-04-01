#!/usr/local/opt/python@3.8/bin/python3
"""This script looks to see what your python3 path is and attempts to replace
the shebang at the top of each file with the proper path.  
USE AT YOUR OWN RISK. Backup folder first!
"""
import sys
import glob, os

def shebang():
    if not "_" in os.environ:
        print("Error: couldn't find path in os.environ")
        sys.exit()
    pypath = os.environ["__PYVENV_LAUNCHER__"]
    shebang = f"#!{pypath}"

    # simple test to make sure path exists
    # not fullproof
    if not "python3" in shebang:
        print(f"Shebang seems wrong! Check: {shebang}")
        #sys.exit()
    return shebang


def prepend_shebang(path):
    replace = False
    with open(path, "r+") as f:
        a = f.read()

    if "#!" in a:
        replace = True

    with open(path, "w+") as f:
        if replace:
            lines = a.split("\n")
            del lines[0]
            a = "\n".join(lines)
        f.write(shebang()+"\n" + a)


if __name__=="__main__":

    path = None
    if len(sys.argv) > 1:
        path = sys.argv[1]

    cwd = os.path.dirname(os.path.abspath(__file__))

    if path != None:
        os.chdir(path)
    else:
        os.chdir(cwd) 
        path = cwd

    for file in glob.glob("*.py"):
        print(os.path.join(path,file))
        prepend_shebang(os.path.join(path,file))