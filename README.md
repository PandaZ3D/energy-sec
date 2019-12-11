This project lives in the contiki test directory: contiki-ng/tests/21-energy-security/

The project contains two tests:
* 01-base-udp-network.csc
* 02-dtls-udp-network.csc

00-example-topology.csc is just a simple hello-world example.

They perform the same experiment with the same measurements, except one runs with the security overhead of DTLS v1.2 and the other without.

Simulations are manually created on Cooja through the contiki-ng container and the configuration is saved to a .csc file. A .csc is essentially an XLM file with all of the mote configurations such as device type, position, etc. It also contains other configurations for the network environment such as transmission range.

# Usage
To run a single test:
$ cd tests/21-energy-security
$ make 01-base-udp-network.testlog
Running test 01-base-udp-network with random Seed 1.................... OK

To run a whole experiment (100 simulations):
$ sh run.sh dtls
Running 02-dtls-udp-network.csc
Simulation 1 in progress