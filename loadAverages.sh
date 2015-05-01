#!/usr/bin/sh

X=`uptime | sed 's/.*average: *//' | sed 's/,//g'`

LEFT=`echo $X | awk '{print $1}'`
CENTER=`echo $X | awk '{print $2}'`
RIGHT=`echo $X | awk '{print $3}'`

echo "load average (1 min)	${LEFT}"
echo "load average (5 min)	${CENTER}"
echo "load average (15 min)	${RIGHT}"
