#!/bin/sh

python3 actuasim/actuasim.py &
sudo python3 beacons/KNX_rest/server.py 
