A Contiki-NG module that periodically prints energest times.
Estimates energy consumption through power estimation timers.
Periodically communicates with other nodes through UDP.

This example runs a full IPv6 stack with 6LoWPAN and RPL.
It is possible, for example to ping such a node:

```
make TARGET=native && sudo ./hello-world.native
```

Look for the node's global IPv6, e.g.:
```
[INFO: Native    ] Added global IPv6 address fd00::302:304:506:708
```

And ping it (over the tun interface):
```
$ ping6 fd00::302:304:506:708
PING fd00::302:304:506:708(fd00::302:304:506:708) 56 data bytes
64 bytes from fd00::302:304:506:708: icmp_seq=1 ttl=64 time=0.289 ms
```

This module includes a modified version of the simple-energest module that can be found in the service modules part of contiki-ng.