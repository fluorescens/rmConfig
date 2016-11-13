#!/usr/bin/python

import urllib2
import RPi.GPIO as GPIO
import datetime
from datetime import timedelta
import subprocess
import webbrowser
import time
import sys

#array of sequential to GPIO numbers (since GPIO not sequential, missing some)
#This header enables GPIO pins to be addressed sequentally instead of with actual numbers
#This saves needing to send always-zero filler bits like 0 for a ground pin
#Instead, GPIO pins are always addressed in increasing 0-max sequantial order 
#	and a provided mapping handles 0 to the correct real pin mapping. 
gpio_mapping_model2b = [2,3,4,7,8,9,10,11,14,15,17,22,23,24,25,27]


#Input methods for instruments are highly diverse: the data could come in pieces from i2c or SPI or analog in sources.
#The method for extracting data and assigning it to a instrument ID should go here.
#What follows is an example of successfully extracted data ready for offload. 
data_pkg={}
data_pkg[0]=0
data_pkg[1]=255
data_pkg[2]=12





#Pull the data from the cache file. 
URL = 0
PULL_SUCCESS = 1
TIMESTAMP = 2
MAXWAIT = 3
FAILURE = 4
HALTBIT = 5

uploader_prefix="/device_interface/postinst/"

cache_config = []
try:
	with open('pinconfig.conf', 'r') as cachefile:
		cache_config = (cachefile.readlines())		
except:
	print "Cache file could not be found"
	sys.exit()
	


for counter,n in enumerate(cache_config):
	strtemp = n.strip('\n')
	cache_config[counter] = strtemp


try:
	#Configuration is raspi-specific. Other platforms may require tweaking for browser defaults & subprocesses
	#Whichever default browser is called here should be the one with the durable authorization cookie. 
	p1 = subprocess.Popen(['epiphany-browser',cache_config[URL]])
	for key,var in data_pkg.iteritems():
		posturl = cache_config[URL] + uploader_prefix + str(key) + "/" + str(var)
		webbrowser.open(posturl,new=0,autoraise=False)
		time.sleep(5)
	#let slow links settle
	time.sleep(20)
	#kill the browser. 
	p1.kill()
except:
	#handle failure to contact server how you wish.
	#default takes no action and simply tries again next time the script is called 
	pass










		