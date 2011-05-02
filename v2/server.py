import glob
import os
import time
import zmq

from multiprocessing import Process, Array
from scipy.misc import imread
from optparse import OptionParser

def parse_cli():
    parser = OptionParser()
    parser.add_option('-n', '--tasks', dest='tasks', default='tcp://*:1234')
    parser.add_option('-w', '--works', dest='works', default='tcp://*:1233')
    opcoes, args = parser.parse_args()
    return opcoes, args


def serve_to_tasks_generators(address, shared_address):
    context = zmq.Context()
    new_tasks = context.socket(zmq.REP)
    new_tasks.bind(address)
    accept = 1
    while 1:
        msg = new_tasks.recv()
        print msg
        if msg.startswith('NEW'):
            if accept:
                try:
                    task_address = msg.split()[1]
                except IndexError:
                    new_tasks.send('REPEAT')
                else:
                    new_tasks.send('OK')
                    accept = 0
                    shared_address.value = task_address
            else:
                new_tasks.send('WAIT')
        elif msg.startswith('END'):
            new_tasks.send('CLOSE')
            accept = 1
        else:
            new_tasks.send('REPEAT')


def serve_to_workers(address, shared_address):
    context = zmq.Context()
    workers_socket = context.socket(zmq.REP)
    workers_socket.bind(address)

    while 1:
        msg = workers_socket.recv()
        print msg
        if msg.startswith('GET'):
            if shared_address.value:
                workers_socket.send('ADDRESS %s' % shared_address)
            else:
                workers_socket.send('REPEAT')
        else:
            workers_socket.send('REPEAT')


def main():
    opcoes, args = parse_cli()
    tasks_address = opcoes.tasks
    works_address = opcoes.works

    shared_address = Array('c', 256)

    pg = Process(target=serve_to_tasks_generators, args=(tasks_address,
                                                         shared_address))
    pg.start()

    pw = Process(target=serve_to_workers, args=(works_address, shared_address))
    pw.start()


if __name__ == '__main__':
    main()
