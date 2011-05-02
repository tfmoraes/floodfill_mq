import glob
import os
import time
import zmq

from multiprocessing import Process
from scipy.misc import imread
from optparse import OptionParser

def parse_cli():
    parser = OptionParser()
    parser.add_option('-i', '--input', dest='input_dir', default='fatias')
    parser.add_option('-o', '--output', dest='output_dir', default='fatias')
    parser.add_option('-a', '--address', dest='address', default='tcp://*:1234')
    parser.add_option('-s', '--server_address', dest='server_address')
    parser.add_option('-t', '--store_address', dest='store_address')
    opcoes, args = parser.parse_args()
    return opcoes, args


def new_task(input_dir, output_dir, address, server_address):
    context = zmq.Context()

    socket_task = context.socket(zmq.REQ)
    socket_task.connect(server_address)

    while 1:
        socket_task.send('NEW %s' % address)
        msg = socket_task.recv()
        if msg == 'OK':
            break
    

    image_send = context.socket(zmq.PUSH)
    image_send.bind(address)

    for arq in glob.glob(os.path.join(input_dir, '*')):
        img = imread(arq)
        image_send.send_pyobj(img)

    while 1:
        pass


def main():
    opcoes, args = parse_cli()
    input_dir = opcoes.input_dir
    output_dir = opcoes.output_dir
    address = opcoes.address
    server_address = opcoes.server_address
    store_address = opcoes.store_address

    pn = Process(target=new_task, args=(input_dir, output_dir, address,
                                       server_address))
    pn.start()

if __name__ == '__main__':
    main()
