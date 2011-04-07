import time
import zmq

from optparse import OptionParser
from multiprocessing import Process, cpu_count

from floodfill import flood_fill_horiz

def parse_cli():
    parser = OptionParser()
    parser.add_option('-a', '--address', dest='address', default='tcp://*:1324')
    opcoes, args = parser.parse_args()
    return opcoes, args


def resolver(name, address):
    context = zmq.Context()
    image_send = context.socket(zmq.PULL)
    image_send.connect(address)

    while True:
        img = image_send.recv_pyobj()
        flood_fill_horiz(img + 255, '/tmp/output.png', 0, 0)


def main():
    opcoes, args = parse_cli()
    address = opcoes.address

    resolvers = range(cpu_count())

    for r in resolvers:
        Process(target=resolver, args=(r, address,)).start()

if __name__ == '__main__':
    main()
