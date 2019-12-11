#!/bin/bash

usage()
{
	echo "usage: $# $0 dtls | udp"
	exit 1
}

UDP="01-base-udp-network"
DTLS="02-dtls-udp-network"
TEST="00-example-topology"

if [[ $# -lt 1 ]]; then
	usage	
else
	if [[ $1 == "udp" ]]; then
		TEST=$UDP
	elif [[ $1 == "dtls" ]]; then
		TEST=$DTLS
	else
		usage
	fi
fi

times=10
count=0

counter=1
while [ $counter -le $times ]
do
	make $TEST".testlog"
	mv "$TEST.1.scriptlog" "data/test-$TEST-$counter.csv"
	counter=$((counter+1))
done