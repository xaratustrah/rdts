#!/usr/bin/env python
"""
A client/server code for Raspberry Pi as a distributed trigger box

Xaratustrah
2016

"""

import datetime, time
import argparse
import zmq
import os
from version import __version__

if os.name == 'posix' and os.uname().machine == 'armv7l':
    try:
        import RPi.GPIO as gpio
    except RuntimeError:
        print("""Error importing RPi.GPIO!  This is probably because you need superuser privileges.
                You can achieve this by using 'sudo' to run your script""")

# sleep time in seconds
SLEEP_TIME = 0.5

# Assing GPIO pin numbers

# Output pins
OUTP = 31

# Input pins
INPT = 33


def gpio_setup():
    # turn off warnings
    gpio.setwarnings(False)
    # we need board numbering system
    gpio.setmode(gpio.BOARD)
    gpio.setup(OUTP, gpio.OUT)
    gpio.setup(INPT, gpio.IN)


def start_server(host, port):
    context = zmq.Context()
    sock = context.socket(zmq.PUB)

    print("tcp://{}:{}".format(host, port))
    sock.bind("tcp://{}:{}".format(host, port))

    topic = '10002'  # just a number for identification
    # check time
    current_time = datetime.datetime.now().strftime('%Y-%m-%d@%H:%M:%S.%f')
    messagedata = current_time
    sock.send_string("{} {}".format(topic, messagedata))
    print("{} {}".format(topic, messagedata))


def do_trigger():
    gpio.output(OUTP, gpio.HIGH)
    time.sleep(SLEEP_TIME)
    gpio.output(OUTP, gpio.LOW)


def start_client(host, port):
    # setup GPIO
    gpio_setup()
    context = zmq.Context()
    print('Client started. ctrl-c to abort.\n')
    try:
        sock = context.socket(zmq.SUB)
        sock.connect("tcp://{}:{}".format(host, port))
        topic_filter = '10002'
        sock.setsockopt_string(zmq.SUBSCRIBE, topic_filter)

        while True:
            string = sock.recv().decode("utf-8")
            current_time = datetime.datetime.now().strftime('%Y-%m-%d@%H:%M:%S.%f')
            do_trigger()
            print("Server time: {}, client time: {}".format(string, current_time))


    except(ConnectionRefusedError):
        print('Server not running. Aborting...')

    except(EOFError, KeyboardInterrupt):
        print('\nUser input cancelled. Aborting...')


def main():
    parser = argparse.ArgumentParser(prog='rasdaq')
    parser.add_argument('--host', nargs=1, type=str, help='Host address', default='127.0.0.1')
    parser.add_argument('--port', nargs=1, type=int, help='Port number', default=1234)
    parser.add_argument('--version', action='version', version=__version__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--client', action='store_true', help='Start client')
    group.add_argument('--server', action='store_true', help='Start server')
    parser.set_defaults(server=False)
    parser.set_defaults(client=False)

    args = parser.parse_args()
    # check the first switches

    if isinstance(args.host, list):
        host = args.host[0]
    else:
        host = args.host

    if isinstance(args.port, list):
        port = args.port[0]
    else:
        port = args.port

    if args.server:

        start_server(host, port)

    elif args.host:
        start_client(host, port)

    else:
        parser.print_help()


# ----------------------------

if __name__ == '__main__':
    main()
