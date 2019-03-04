import subprocess
import hashlib
import glob
import itertools
from time import sleep
from skds.log import timeit
import datetime

PATH = '.'


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
    exts = ['lr']
    for ext in exts:
        yield glob.glob(f'{root}/**/*.{ext}', recursive=True)


# todo: figure out how to use actual api instead of invoking like this
def trigger_build():
    return subprocess.run("lektor build -O build", shell=True)


def check_hashes(state, files):
    _state = {}
    reload = False
    for path in files:
        contents = read_file(path)
        if contents is not None:
            _state[path] = _hash(contents)
            if _state[path] != state[path] or path not in state:
                print(datetime.datetime.now(), f"{path} changed")
                state[path] = _state[path]
                reload = True

    if reload:
        trigger_build()
        trigger_copy(PATH)


def take_first_pod(filter=None):
    pods = subprocess.run("kubectl get pods -o name", shell=True, capture_output=True).stdout.decode().split()
    if filter is not None:
        pods = [p.replace('pod/', '') for p in pods if filter in p and 'themes' not in p]
        print(datetime.datetime.now(), pods)
    return pods[0]


@timeit
def trigger_copy(path):
    pod = take_first_pod(filter="zigdata")
    cmd_copy = f"cd build && echo $(ls) && kubectl cp {path} {pod}:/var/www/zigdata && cd .."
    cmd_exec = f"kubectl exec {pod} -- /bin/ash -c 'cp -ar /var/www/zigdata/zigdata/* /var/www/zigdata'"
    combined = ' && '.join((cmd_copy, cmd_exec))
    print(combined)
    subprocess.run(combined, shell=True)


if __name__ == "__main__":
    files = list(itertools.chain(*get_html_files()))
    state = dict.fromkeys(files)
    while True:
        check_hashes(state, files)
        sleep(0.5)
