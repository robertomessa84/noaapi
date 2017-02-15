#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################################
#     Noaa PI
#     Copyright 2017 by Roberto Messa <roberto.messa@ilampidigenio.it>
#   
#     Please refer to the LICENSE file for conditions 
#     Visit http://www.ilampidigenio.it
# 
##########################################################################

import sys
import time
import os

"""     Main program """

################################  functions############################
def getDataOraInizioFile(nomeSatellite):
	_tmp = os.popen("/usr/bin/predict -t ./predict/weather.tle -p '%s' | head -1" % nomeSatellite).read() 
	_str = _tmp.split()
	
	_data = _str[2]
	_ora = _str[3]

	return _data, _ora
	
def getDataOraFineFile(nomeSatellite):
	_tmp = os.popen("/usr/bin/predict -t ./predict/weather.tle -p '%s' | tail -1" % nomeSatellite).read() 
	_str = _tmp.split()
	
	_data = _str[2]
	_ora = _str[3]
	
	return _data, _ora

def getElevazioneMassima(nomaSatellite):
	#Restitusce la massima elevazione del satellite.
	return os.popen("/usr/bin/predict -t ./predict/weather.tle -p %s' | awk -v max=0 '{if($5>max){max=$5}}END{print max}'" % nomeSatellite).read() 
	
def getDatiFromSatellite(nomeSatellite, frequenza):
	#Legge i dati dal satellite indicato utilizzando la frequenza indicata per la sintonizzazione.
	_datainiz, _orainiz = getDataOraInizioFile(nomeSatellite)
	_datafine, _orafine = getDataOraFineFile(nomeSatellite)
	_elevazioneMassima = getElevazioneMassima(nomeSatellite)
		
	#Controllo se sono presenti dei record nella data corrente.
	#now = datetime.datetime.now()
	_datefine_object = datetime.strptime(_datafine, '%b%d%Y')
	while datetime.datetime.now() == _datafine_object:
		#posso elaborare i dati del satellite
			
		if _elevazioneMassima > 19:
			#echo ${1//" "}${OUTDATE} $MAXELEV
			#echo "./predict/receive_and_process_satellite.sh \"${1}\" $2 /home/pi/weather/${1//" "}${OUTDATE} /home/pi/weather/predict/weather.tle $var1 $TIMER" | at `date --date="TZ=\"UTC\" $START_TIME" +"%H:%M %D"`
			os.system("./predict/receive_and_process_satellite.sh \"'%s'\" $2 ./${1//" "}${OUTDATE} ./predict/weather.tle $var1 $TIMER" % nomeSatellite)
			
def getPosizioneSatelliti():
	#Scarica le posizioni aggiornate dei satelliti.
	print "Scarico le posizioni aggiornate dei satelliti da internet"
	os.system("sudo ./predict/update_satellite.sh")

# Load Configuration
#configfile = 'swpi.cfg'
#if not os.path.isfile(configfile):
#	cfg = config.config(configfile,False)
#	os.system( "sudo chown pi swpi.cfg" )
#
#	log("Configurantion file created with default option. Now edit the file :  %s and restart with command  : swpi "  % (configfile))
#	#exit(0)
#else:
#	cfg = config.config(configfile,False)
	

##################################################################################
#v = version.Version("VERSION").getVersion()
v = "01.00"
#log( "Starting NOAA PI  ... ")
############################ MAIN ###############################################
print "************************************************************************"
print "*                         NOAA PI "+v+"                                *"
print "*                                                                      *"
print "*   2016-2017 by Roberto Messa <roberto.messa@ilampidigenio.it>        *"
print "*                                                                      *"
print "*     System will start in 10 seconds - Press Ctrl-C to cancel         *"
print "************************************************************************"
# Get curret log file
#globalvars.TimeSetFromNTP = False
#globalvars.logFileDate = datetime.datetime.now().strftime("%d%m%Y")
#logFileDate = datetime.datetime.now().strftime("%d%m%Y")

SecondsToWait = 10
# give 10 seconds for interrupt the application
try:
	if not ( '-i' in sys.argv ) :
		for i in range(0,SecondsToWait):
			sys.stdout.write(str(SecondsToWait-i) + ".....")
			sys.stdout.flush()
			time.sleep(1)
		print ""
except KeyboardInterrupt:
	#print  "Stopping noaa"
	exit(0)

#Make sure every executable is executable
os.system( "sudo chmod +x ./predict/receive_and_process_satellite.sh" )
os.system( "sudo chmod +x ./predict/update_satellite.sh" )

#Scarico le posizioni aggiornate dei satelliti da internet
getPosizioneSatelliti()

# Start main thread
############################ MAIN  LOOP###############################################
#TODO: - Gestire Upload dei file di immagine via FTP.
#	   - Scaricare i file da tutti e 3 i satelliti.
#	   - Gestire correttamente il file di log
#	   - Gestire file di configurazione
while 1:

	try:	
	#os.system("sudo ./wifi_reset.sh")
		print "Controllo se stanno per passare i satelliti NOAA 15, NOAA 18 e NOAA 19"

		#Comandi per leggere i dati.
		#/home/pi/weather/predict/schedule_satellite.sh "NOAA 19" 137.1000
		getDatiFromSatellite("NOAA 19", 137.1000)
		
		#/home/pi/weather/predict/schedule_satellite.sh "NOAA 18" 137.9125
		#getDatiFromSatellite("NOAA 18", 137.9125)
		
		#/home/pi/weather/predict/schedule_satellite.sh "NOAA 15" 137.6200
		#getDatiFromSatellite("NOAA 15", 137.6200)
				
		#la data non è più valida devo riscaricare le definizioni.
		#getPosizioneSatelliti()
		
	except KeyboardInterrupt:
		exit(0)
	
	except Exception,e:
		print e.message
		print e.__class__.__name__
		#traceback.print_exc(e)
			
	





