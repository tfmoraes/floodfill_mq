import time
import zmq

from optparse import OptionParser

def parse_cli():
    parser = OptionParser()
    parser.add_option('-i', '--input', dest='input_dir', default='fatias')
    parser.add_option('-o', '--output', dest='output_dir', default='fatias')
    parser.add_option('-a', '--address', dest='address', default='tcp://*:1324')
    opcoes, args = parser.parse_args()
    return opcoes, args


def serve(input_dir, output_dir, address):
    context = zmq.Context()

    image_send = context.socket(zmq.PUSH)
    image_send.bind(address)

    print "Conectou"

def main():
    opcoes, args = parse_cli()
    input_dir = opcoes.input_dir
    output_dir = opcoes.output_dir
    address = opcoes.address

    serve(input_dir, output_dir, address)

if __name__ == '__main__':
    main()
