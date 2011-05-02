import time
import zmq

from optparse import OptionParser
from multiprocessing import Process, cpu_count

from floodfill import flood_fill_horiz

def parse_cli():
    parser = OptionParser()
    parser.add_option('-a', '--address', dest='address', default='tcp://*:1234')
    opcoes, args = parser.parse_args()
    return opcoes, args


def resolver(name, address):
    context = zmq.Context()

    task_socket = context.socket(zmq.REQ)
    task_socket.connect(address)

    while 1:
        task_socket.send('GET')
        msg = task_socket.recv()
        print msg
        if msg.startswith('ADDRESS'):
            task_address = msg.split()[1]
            break

    image_send = context.socket(zmq.PULL)
    print "Connecting to", address
    image_send.connect(task_address)
    print "Connected"

    while True:
        img = image_send.recv_pyobj()
        print "Resolving a new image"
        flood_fill_horiz(img, '/tmp/output.png', 0, 0)


def main():
    opcoes, args = parse_cli()
    address = opcoes.address

    resolvers = range(cpu_count())

    for r in resolvers:
        Process(target=resolver, args=(r, address,)).start()

if __name__ == '__main__':
    main()
