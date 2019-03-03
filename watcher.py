import subprocess
import os
import hashlib
import glob
from collections import defaultdict
from time import sleep
from skds.log import timeit
import datetime

PATH = 'apps/blog'


def _hash(s):
    return hashlib.md5(s.encode()).hexdigest()


def read_file(path):
    try:
        with open(path) as f:
            text = f.read()
    except:
        text = None
    return text

def get_html_files(root=PATH):
    return glob.glob(f'{root}/**/*.html', recursive=True)

def check_hashes(state):
    files = get_html_files()
    _state = {}
    for path in files:
        contents = read_file(path)
        if contents is not None:
            _state[path] = _hash(contents)
            if _state[path] != state[path]:
                print(datetime.datetime.now(), f"{path} changed")
                state[path] = _state[path]
                yield path

# todo: make efficient if needed
def get_pods(filter=None):
    pods = subprocess.run("kubectl get pods -o name", shell=True, capture_output=True).stdout.decode().split()
    if filter is not None:
        pods = [p.replace('pod/', '') for p in pods if filter in p and 'themes' not in p]
        print(datetime.datetime.now(), pods)
    if len(pods) > 0:
        pass
        # print(datetime.datetime.now(), 'warning, more than one pod detected, taking first')
    return pods[0]

def trigger_copy(path):
    pod = get_pods(filter="zigdata")
    cmd = f"kubectl cp {path} {pod}:/var/www/zigdata/"
    print(datetime.datetime.now(), cmd)
    subprocess.run(cmd, shell=True)


if __name__ == "__main__":
    state = dict.fromkeys(get_html_files())
    while True:
        changed = list(check_hashes(state))
        if len(changed) > 0:
            trigger_copy('/'.join((PATH, "zigdata", "build")))
        sleep(3)
