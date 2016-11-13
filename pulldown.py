#!/usr/bin/python

import urllib2
import RPi.GPIO as GPIO
from array import *
import datetime
from datetime import timedelta
import subprocess

#Set the reciever ID that will be used for configuration pulls for this device. 
THIS_DEVICE_ID = 0

#array of sequential to GPIO numbers (since GPIO not sequential, missing some)
#This header enables GPIO pins to be addressed sequentally instead of with actual numbers
#This saves needing to send always-zero filler bits like 0 for a ground pin
#Instead, GPIO pins are always addressed in increasing 0-max sequantial order 
#	and a provided mapping handles 0 to the correct real pin mapping. 
gpio_mapping_model2b = [2,3,4,7,8,9,10,11,14,15,17,22,23,24,25,27]


#initial GPIO header; declare output pins here
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#GPIO.setup(2,GPIO.OUT)
#GPIO.setup(3,GPIO.OUT)
#GPIO.setup(4,GPIO.OUT)
#GPIO.setup(7,GPIO.OUT)




#Pull the data from the cache file. 
URL = 0
PULL_SUCCESS = 1
TIMESTAMP = 2
MAXWAIT = 3
FAILURE = 4
HALTBIT = 5

postfix_url = "/device_interface/rec_bin/"

cache_config = []
try:
	with open('pinconfig.conf', 'r') as cachefile:
		cache_config = (cachefile.readlines())		
except:
	print "Find or open cache failure."


for counter,n in enumerate(cache_config):
	strtemp = n.strip('\n')
	cache_config[counter] = strtemp



#IF haltbit set, this code will take not action. default configuation is locked
#User with authorized file access must disable the lockup

if cache_config[HALTBIT] == "1":
	print "Entered lockup state at " + cache_config[TIMESTAMP]
	print "Manually reset the lockup bit in the configuration file to 0."
else:
	#run program
	try:
		#request configuration page
		#urlib doesn't import authorization token stored in initial setup browser cache
		#this number can be afforded other encryptions such as synchronized XOR. 
		#	or sent in plaintext, since get pages cannot alter any server side data
		#implementation security requirements will vary. Decide accordingly. 
		geturl = cache_config[URL] + postfil_url + str(THIS_DEVICE_ID)
		pulled = urllib2.urlopen(geturl).read()
		evaluation = int(pulled)
		counter = 0
		while evaluation > 0:
			if evaluation&1 == 1:
				#print "PIN : " + str(counter) + " UP"
				GPIO.output(gpio_mapping_model2b[counter],GPIO.HIGH)
			else:
				#print "PIN : " + str(counter) + " DOWN"
				GPIO.output(gpio_mapping_model2b[counter],GPIO.LOW)
			evaluation = evaluation >> 1
			counter = counter + 1

		#successfully write updates to cache file.
		cache_config[PULL_SUCCESS] = pulled
		cache_config[TIMESTAMP] = datetime.datetime.now() 
	except:
		last_checkin = datetime.datetime.strptime(cache_config[2], '%Y-%m-%d %H:%M:%S.%f')
	
		evaluation = int(cache_config[PULL_SUCCESS])
		counter = 0

		if datetime.datetime.now() > (last_checkin + timedelta(seconds=int(cache_config[3]))):
			#Failed to acquire URL and waiting period expired
			print "Lockup triggered at " + str(datetime.datetime.now())
			cache_config[HALTBIT] = "1"
			cache_config[TIMESTAMP] = datetime.datetime.now()

			#put all pins onto the default state 
			evaluation = int(cache_config[FAILURE])	

		else:
			#"Failed to acquire URL. Running on last known good pull"
			pass
		#set pins to their default configuration. 
		for n in gpio_mapping_model2b:
			if evaluation&1 == 1:
				#print "PIN : " + str(counter) + " UP"
				GPIO.output(gpio_mapping_model2b[counter],GPIO.HIGH)
			else:
				#print "PIN : " + str(counter) + " DOWN"
				GPIO.output(gpio_mapping_model2b[counter],GPIO.LOW)
			evaluation = evaluation >> 1
			counter = counter + 1

	#write back to cache file. 
	try:
		writeout = open('pinconfig.conf','w')
		for data in cache_config:
			writeout.write(str(data)+'\n')
	except:
		pass
	

		