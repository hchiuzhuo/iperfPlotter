#!/bin/bash

#plot all lines in testTarball
# python3 iperf3_plot.py -f ./testTarball  -o graph/all.png

#plot all lines in testTarball with boundary
python3 iperf3_plot.py -f testTarball \
 -o graph/all.png \
 -b [0.42,0.42,0.42M],[0.46,0.46,0.46M] \
 -u 0.5 \
 -l 0.45

#plot tg_server_00004,tg_server_00009 in testTarball
# python3 iperf3_plot.py -f testTarball \
#  -o graph/s49.png \
#  -p tg_server_00004,tg_server_00009

#plot tg_server_00004,tg_server_00009 in testTarball, plot boundary on indifidual line.
# python3 iperf3_plot.py -f testTarball \
#  -o graph/s49_bound.png \
#  -p tg_server_00004,tg_server_00009 \
#  -u 0.5 \
#  -l 0.45 

#plot all lines in testTarball except tg_server_00004,tg_client_00009 
# python3 iperf3_plot.py -f testTarball \
#  -o graph/s1419.png \
#  -n tg_server_00004,tg_server_00009

#plot all lines in testTarball except tg_server_00009 
# python3 iperf3_plot.py -f testTarball \
#  -o graph/s09.png \
#  -n tg_server_00009 \
#  -u 0.5 \
#  -l 0.45




