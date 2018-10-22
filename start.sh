#!/bin/sh

python3 IOT/actuasim/actuasim.py &
sudo python3 IOT/IOT/beacons/KNX_rest/server.py 
