#!/usr/bin/env python
"""
A trigger with a timer. Triggers every XXX seconds and records the times in a log file.

Xaratustrah
2021

"""

import datetime
import time
import argparse
import os
from version import __version__

if os.name == 'posix' and os.uname().machine == 'armv7l':
    try:
        import RPi.GPIO as gpio
    except RuntimeError:
        print("""Error importing RPi.GPIO!  This is probably because you need superuser privileges.
                You can achieve this by using 'sudo' to run your script""")


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


def start_trigger(trig_time, logfile):
    gpio_setup()
    print('Triggering every {}. Press ctrl-c to abort.'.format(trig_time))
    f = open(logfile, "a")
    try:
        while True:
            current_time = datetime.datetime.now().strftime('%Y-%m-%d@%H:%M:%S.%f')
            print('Triggering at: {}'.format(current_time))
            do_trigger()
            time.sleep(trig_time)
            f.write(current_time + '\n')
    except(EOFError, KeyboardInterrupt):
        print('\nUser input cancelled. Aborting...')
        f.close()


def main():
    parser = argparse.ArgumentParser(prog='trigtimer')
    parser.add_argument('--logfile', nargs=1, type=str,
                        help='name of the logfile', default='trigtimer.log')
    parser.add_argument('--time', nargs=1, type=int,
                        help='Trigger time in seconds', default=5)
    parser.add_argument('--version', action='version', version=__version__)

    args = parser.parse_args()
    # check the first switches
    trigtime = int(args.time[0])
    if isinstance(args.logfile, list):
        logfile = args.logfile[0]
    else:
        logfile = args.logfile

    start_trigger(trigtime, logfile)

# ----------------------------


if __name__ == '__main__':
    main()
