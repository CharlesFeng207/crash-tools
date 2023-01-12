import os
import time
import sys
import subprocess
from tqdm import tqdm
from arm64 import *
# from arm32 import *


time_str = time.strftime("%Y-%m-%d-%H-%M-%S")
file_path = f"dumps\\{time_str}.log" 
folder = sys.argv[0]
print(file_path)


def append_to_file(txt):
    f = open(file_path, 'a+')
    f.write(str(txt) + "\n")
    f.close()
    pass  

cache = {}
def fetch_addr2line(args):
    if args in cache:
        return cache[args]
    cmd = f"{tool_path} -f -C -s -p -e {args}"
    result = subprocess.check_output(cmd, shell=True)
    cache[args] = result
    return result


def find_lib(lib):
    slib = list(all_libs.keys())[0]
    for t in all_libs:
        if t in lib:
            slib = t
            pass
        pass
    return slib

# (lib, method)
def parse(line):
    a = line.strip().replace("(Native Method)", "").split()
    if len(a) < 2:
        return None

    if "lib" in a[0]:
        return (find_lib(a[0]),a[1])
    else:
        return (find_lib(a[1]),a[0])
    pass




lines = []
with open('origin.txt') as f:
    lines = f.readlines()
    pass

result = ""
for line in tqdm (lines, desc="Analyzing..."):
    t = parse(line)
    if t is None:
        append_to_file(line)
        continue
    lib, method = t
    args = f"\"{all_libs[lib]}\" {method}"
    result = fetch_addr2line(args)
    append_to_file(result)

os.system(file_path)


