# RDTS - Raspberry Pi Distributed Trigger System

![RDTS](https://raw.githubusercontent.com/xaratustrah/rdts/master/rsrc/rdts.png)

RDTS is a scalable hardware triggering system for data acquisition devices such as data loggers, oscilloscopes or spectrum analysers. The output can be used in order to trigger several devices.

The code also provides a delayed trigger exactly half of the assigned value. This feature allows for alternate triggering of two devices that are monitoring the same signal.

The code can be operated in stand alone mode for manual or time based trigger. In the client / server mode, many devices can be triggered at once.


#### Installation
After cloning the code of the repository, go inside that directory and type:

```
pip install -r requirements.txt
pip3 install .
```

or uninstall

```
pip3 uninstall rdts
```


#### Stand alone trigger: `rdts_cliserv`

This is a stand alone trigger machine that triggers every XXX seconds and writes the trigger times in a log file, where XXX is a value that you enter int the command line. Trigger every 2 seconds and record the times in a log file:

```
rdts_timer --time 2 --logfile test.txt
```

You can interrupt the trigger by pressing `ctrl-C`. By doing so, one last trigger will be issued. So this can be used for single arbitrary triggers, like you set the trigger time to something large, but then break at your wish.

#### Client-Server based remote trigger: `rdtscli`

This one is a client/server code that allows for a distributed trigger box system. The server is run on the the computer. The client on one or many trigger boxes. It accepts only IP addresses not names. Please also provide port numbers. The IP address is the one of the computer. For example:

On the computer you run the server:

```
rdts_cliserv --server --host 192.168.1.3 --port 1434
```

here `host` is the IP address of the computer, who is acting as a server.


on the RDTS you run the client:

```
rdts_cliserv --client --host 192.168.1.3 --port 1434
```

here the same information as above, that is, the IP address and port numnber of the server is given.


## Licensing

Please see the file [LICENSE.md](./LICENSE.md) for further information about how the content is licensed.

## Acknowledgements

Many thanks to Davide Recano for providing help with the mechanical preparation of the enclosure.