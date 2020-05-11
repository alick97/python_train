# coprocess.py
#
# An example of running a coroutine in a subprocess connected by a pipe

# try:
#     import cPickle as pickle
# except Exception:
#     import pickle
import json
from coroutine import *

@coroutine
def sendto(f):
    try:
        while True:
            item = (yield)
            # print('dump item:', type(item))
            # pickle.dump(item, f)
            # f.flush()
            f.write(json.dumps(item).encode('utf-8'))
            f.write('\n'.encode('utf-8'))
            f.flush()
    except StopIteration:
        f.close()

def recvfrom(f,target):
    try:
        while True:
            # item = pickle.load(f)
            item = f.readline()
            if item.strip() == '':
                continue
            # print('===== recvfrom item: {}, type: {}'.format(item, type(item)))
            target.send(json.loads(item))
    except EOFError:
        target.close()


# Example use
if __name__ == '__main__':
    import xml.sax
    from cosax import EventHandler
    from buses import *

    import subprocess
    p = subprocess.Popen(['python','busproc.py'],
                         stdin=subprocess.PIPE)

    xml.sax.parse("/home/alick/workspace/zulip_t/tornado_t/allroutes.xml",
                  EventHandler(
                          buses_to_dicts(
                          sendto(p.stdin))))
