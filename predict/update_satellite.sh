#!/bin/bash

# Update Satellite Information

wget -qr https://www.celestrak.com/NORAD/elements/weather.txt -O ./predict/weather.txt
grep "NOAA 15" ./predict/weather.txt -A 2 > ./predict/weather.tle
grep "NOAA 18" ./predict/weather.txt -A 2 >> ./predict/weather.tle
grep "NOAA 19" ./predict/weather.txt -A 2 >> ./predict/weather.tle
grep "METEOR-M 2" ./predict/weather.txt -A 2 >> ./predict/weather.tle

