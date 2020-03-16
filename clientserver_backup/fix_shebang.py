import os,sys
import glob, os

def shebang():
    if not "_" in os.environ:
        print("Error: couldn't find path in os.environ")
        sys.exit()
    pypath = os.environ["_"]
    shebang = f"#!{pypath}"

    if not "python3" in shebang:
        print(f"Shebang seems wrong! Check: {shebang}")
        sys.exit()
    return shebang


def prepend_shebang(path):
    with open(path, "r+") as f:
        a = f.read()
    with open(path, "w+") as f:
        f.write("line to append" + a)

cwd = os.path.dirname(os.path.abspath(__file__))



print(shebang)

os.chdir(cwd)

for file in glob.glob("*.py"):
    print(file)


