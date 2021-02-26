#!/usr/bin/env python
"""
A trigger with a timer

Xaratustrah
2021

"""

import datetime
import time
import argparse
import os
from version import __version__


# duration times in seconds
TRIGGER_DURATION = 0.1
BEEP_DURATION = 0.2

# Assing GPIO pin numbers

# Output pins
TRIG_IN = 8

# Input pins
BEEP = 32
TRIG_OUT = 38


def gpio_setup():
    # turn off warnings
    gpio.setwarnings(False)
    # we need board numbering system
    gpio.setmode(gpio.BOARD)
    gpio.setup(TRIG_IN, gpio.IN)

    gpio.setup(TRIG_OUT, gpio.OUT)
    gpio.output(TRIG_OUT, gpio.LOW)
    gpio.setup(BEEP, gpio.OUT)
    gpio.output(BEEP, gpio.LOW)


def do_trigger():
    gpio.output(TRIG_OUT, gpio.HIGH)
    time.sleep(TRIGGER_DURATION)
    gpio.output(TRIG_OUT, gpio.LOW)

    gpio.output(BEEP, gpio.HIGH)
    time.sleep(BEEP_DURATION)
    gpio.output(BEEP, gpio.LOW)


def start_trigger(trig_time):
    print('Triggering every {}. Press ctrl-c to abort.'.format(trig_time))
    try:
        while True:
            do_trigger()
            time.sleep(trig_time)
    except(EOFError, KeyboardInterrupt):
        print('\nUser input cancelled. Aborting...')


def main():
    parser = argparse.ArgumentParser(prog='trigtimer')
    parser.add_argument('--time', nargs=1, type=int,
                        help='Trigger time in seconds', default=5)
    parser.add_argument('--version', action='version', version=__version__)

    args = parser.parse_args()
    # check the first switches
    trigtime = int(args.time)
    start_trigger(trigtime)

# ----------------------------


if __name__ == '__main__':
    main()
