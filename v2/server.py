import glob
import os
import time
import zmq

from multiprocessing import Process
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
                new_tasks.send('OK')
                accept = 0
            else:
                new_tasks.send('WAIT')
        elif msg.startswith('END'):
            new_tasks.send('CLOSE')
            accept = 1
        else:
            new_tasks.send('REPEAT')


def main():
    opcoes, args = parse_cli()
    tasks_address = opcoes.tasks
    works_address = opcoes.works

    pg = Process(target=serve_to_tasks_generators, args=(tasks_address,))
    pg.start()

if __name__ == '__main__':
    main()
