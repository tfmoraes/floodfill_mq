import time
import zmq

from optparse import OptionParser
from multiprocessing import Process, cpu_count

def parse_cli():
    parser = OptionParser()
    parser.add_option('-a', '--address', dest='address', default='tcp://*:1324')
    opcoes, args = parser.parse_args()
    return opcoes, args


def resolver(input_dir, output_dir, address):
    context = zmq.Context()
    image_send = context.socket(zmq.PULL)
    image_send.connect(address)
    print "Conectou"

def main():
    opcoes, args = parse_cli()
    address = opcoes.address

    resolvers = range(cpu_count())

    for r in resolvers:
        Process(target=resolver, args=(input_dir, output_dir, address)).start()

if __name__ == '__main__':
    main()
