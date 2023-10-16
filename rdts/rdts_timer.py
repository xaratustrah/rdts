#!/usr/bin/env python
"""
A trigger with a timer. Triggers every XXX seconds and records the times in a log file.

xaratustrah

2021
2023

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
BEEP = 38
TRIG_OUT1 = 32
TRIG_OUT2 = 36


def gpio_setup():
    # turn off warnings
    gpio.setwarnings(False)
    # we need board numbering system
    gpio.setmode(gpio.BOARD)
    gpio.setup(TRIG_IN, gpio.IN)

    gpio.setup(TRIG_OUT1, gpio.OUT)
    gpio.output(TRIG_OUT1, gpio.LOW)

    gpio.setup(TRIG_OUT2, gpio.OUT)
    gpio.output(TRIG_OUT2, gpio.LOW)

    gpio.setup(BEEP, gpio.OUT)
    gpio.output(BEEP, gpio.LOW)


def do_trigger_first():
    gpio.output(TRIG_OUT1, gpio.HIGH)
    time.sleep(TRIGGER_DURATION)
    gpio.output(TRIG_OUT1, gpio.LOW)

    gpio.output(BEEP, gpio.HIGH)
    time.sleep(BEEP_DURATION)
    gpio.output(BEEP, gpio.LOW)

def do_trigger_second():
    gpio.output(TRIG_OUT2, gpio.HIGH)
    time.sleep(TRIGGER_DURATION)
    gpio.output(TRIG_OUT2, gpio.LOW)

def start_trigger(trig_time, logfile):
    gpio_setup()
    print('Triggering every {} seconds. Otherwise press ctrl-c to trigger once and abort.'.format(trig_time))
    f = open(logfile, "a")
    try:
        # we wait first one whole trig_time
        time.sleep(trig_time)
        while True:
            # first trigger
            current_time = datetime.datetime.now().strftime('%Y-%m-%d@%H:%M:%S.%f')
            print('Triggering at: {}'.format(current_time))
            do_trigger_first()
            time.sleep(trig_time / 2)
            
            # second trigger offset by half of the period
            do_trigger_second()
            time.sleep(trig_time / 2)
            f.write(current_time + '\n')

    except(KeyboardInterrupt, EOFError):
        print('\n\nUser cancelled. Please wait for the last trigger...')
        current_time = datetime.datetime.now().strftime('%Y-%m-%d@%H:%M:%S.%f')
        print('Last trigger issued at: {}'.format(current_time))

        do_trigger_first()
        time.sleep(trig_time / 2)
        do_trigger_second()
        time.sleep(trig_time / 2)
        
        f.write(current_time + '\n')
        print('\nDone.')
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
