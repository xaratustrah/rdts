# RDTS - Raspberry Pi Distributed Trigger System

![RDTS](https://raw.githubusercontent.com/xaratustrah/rdts/master/rsrc/rdts.png)

RDTS is a set of tools for hardware triggering data acquisition devices such as data loggers, oscilloscopes or spectrum analysers. The output can be used in order to trigger several devices.

The code also allows for a delayed trigger exactly half of the assigned value. This feature allows for alternate triggering of two devices that are monitoring the same signal.


#### Installation
You can install the tool just by typing:

```
pip install .
```

#### Stand alone trigger: `rdts_cliserv`

This is a stand alone trigger machine that triggers every XXX seconds and writes the trigger times in a log file, where XXX is a value that you enter int the command line. Trigger every 2 seconds and record the times in a log file:

```
rdts_timer --time 2 --logfile test.txt
```

You can interrupt the trigger by pressing `ctrl-C`. By doing so, one last trigger will be issued. So this can be used for single arbitrary triggers, like you set the trigger time to something large, but then break at your wish.

#### Client-Server based remote trigger: `rdtscli`

This one is a client/server code that allows for a distributed trigger box system. The server is run on the the computer. The client on the trigger box. It accepts only IP addresses not names. Please also provide port numbers.

## Licensing

Please see the file [LICENSE.md](./LICENSE.md) for further information about how the content is licensed.

## Acknowledgements

Many thanks to Davide Recano for providing help with the mechanical preparation of the enclosure.