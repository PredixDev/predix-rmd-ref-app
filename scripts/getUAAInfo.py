
def getVcapJsonForPredixBoot ():
	predixBootEnv = subprocess.check_output(["cf", "env" ,config.predixbootAppName])
	systemProvidedVars=predixBootEnv.split('System-Provided:')[1].split('No user-defined env variables have been set')[0]
	formattedJson = systemProvidedVars.replace("\n","").replace("'","").replace("}{","},{")
	return "["+formattedJson+"]"

def getTokenFromUAA():
	url = uaaIssuerId
	oauthRelam = config.rmdAppClientId+":"+config.rmdAppSecret
	authKey = base64.b64encode(oauthRelam)
	print ( authKey)
	headers = {"Content-Type":"application/x-www-form-urlencoded", "Authorization":"Basic " + authKey}
	#jsonPostBody = "grant_type=password&username=app_admin_1&password=app_admin_1"
	jsonPostBody= "response_type=password&grant_type=client_credentials&client_id=" + config.rmdAppClientId
	print(url , "body " +jsonPostBody +"auth keys "+authKey)
	request = urllib2.Request(url)
	request.add_data(jsonPostBody)
	for key,value in headers.items():
  		request.add_header(key,value)
  	response = urllib2.urlopen(request)	
  	data_respo = response.read()
  	jsonResponse = json.loads(data_respo)
  	return (jsonResponse['token_type']+" "+jsonResponse['access_token'])

def getPredixUAAConfigfromVcaps():
	formattedJson = getVcapJsonForPredixBoot()
	d = json.loads(formattedJson)
	uaaIssuerId =  d[0]['VCAP_SERVICES'][config.predixUaaService][0]['credentials']['issuerId']
	UAA_URI = d[0]['VCAP_SERVICES'][config.predixUaaService][0]['credentials']['uri']
	uaaZoneHttpHeaderName = d[0]['VCAP_SERVICES'][config.predixUaaService][0]['credentials']['zone']['http-header-name']
	uaaZoneHttpHeaderValue = d[0]['VCAP_SERVICES'][config.predixUaaService][0]['credentials']['zone']['http-header-value']
	return (uaaIssuerId ,UAA_URI,uaaZoneHttpHeaderName ,uaaZoneHttpHeaderValue)	

def getPredixACSConfigfromVcaps():
	formattedJson = getVcapJsonForPredixBoot()
	d = json.loads(formattedJson)
	ACS_URI = d[0]['VCAP_SERVICES'][config.predixAcsService][0]['credentials']['uri']
	acsPredixZoneHeaderName = d[0]['VCAP_SERVICES'][config.predixAcsService][0]['credentials']['zone']['http-header-name']
	acsPredixZoneHeaderValue = d[0]['VCAP_SERVICES'][config.predixAcsService][0]['credentials']['zone']['http-header-value']
	acsOauthScope = d[0]['VCAP_SERVICES'][config.predixAcsService][0]['credentials']['zone']['oauth-scope']
	return (ACS_URI,acsPredixZoneHeaderName,acsPredixZoneHeaderValue,acsOauthScope)		

def getClientAuthoritiesforAssetAndTimeSeriesService(formattedVcapJson):
	d = json.loads(formattedJson)
	 
	assetAuthorities = config.predixAssetService+".zones."+d[0]['VCAP_SERVICES'][config.predixAssetService][0]['credentials']['instanceId']+".user"
	#get Ingest authorities	
	tsInjest = d[0]['VCAP_SERVICES'][config.predixTimeSeriesService][0]['credentials']['ingest']
	timeSeriesInjestAuthorities = tsInjest['zone-token-scopes'][0] +"," + tsInjest['zone-token-scopes'][1] 
	# get query authorities
	tsQuery = d[0]['VCAP_SERVICES'][config.predixTimeSeriesService][0]['credentials']['query']
	timeSeriesQueryAuthorities = tsQuery['zone-token-scopes'][0] +"," + tsQuery['zone-token-scopes'][1]
    
	print ("returning timeseries client zone scopes query -->"+timeSeriesQueryAuthorities + " timeSeriesInjestAuthorities -->"+timeSeriesInjestAuthorities )

	return assetAuthorities,timeSeriesInjestAuthorities,timeSeriesQueryAuthorities		

def createPredixCloudIdentityForMachine():
	# copy template as manifest
	shutil.copy("scripts/com.ge.dspmicro.predixcloud.identity.config.template", "scripts/com.ge.dspmicro.predixcloud.identity.config")
	s = open("scripts/com.ge.dspmicro.predixcloud.identity.config").read()
	s = s.replace('${UAAUrl}', uaaIssuerId)
	s = s.replace('${clientId}', config.rmdAppClientId)
	s = s.replace('${clientSecret} ', config.rmdAppSecret)
	
	f = open("scripts/com.ge.dspmicro.predixcloud.identity.config", 'w')
	f.write(s)
	f.close()
	with open('scripts/com.ge.dspmicro.predixcloud.identity.config', 'r') as fin:
		print (fin.read())
#######################################
# Begin Main script
#######################################
import subprocess
import sys,getopt
import os
import json
import urllib
import urllib2
import base64
import random
import string
import shutil
import time
import getopt
import argparse
import installConfig as config

print ('environment : '+config.environment)
print("****************** Fetching UAA/ACS info ******************\n")

formattedJson = getVcapJsonForPredixBoot()
# these two are modified by some other functions.
clientAuthorites = config.clientAuthorites
clientScope = config.clientScope



uaaIssuerId,UAA_URI,uaaZoneHttpHeaderName,uaaZoneHttpHeaderValue = getPredixUAAConfigfromVcaps()
print("****************** UAA configured As ******************")
print ("\n uaaIssuerId = " + uaaIssuerId + "\n UAA_URI = " + UAA_URI + "\n "+uaaZoneHttpHeaderName+" = " +uaaZoneHttpHeaderValue+"\n")
print("****************** ***************** ******************")

ACS_URI,acsPredixZoneHeaderName,acsPredixZoneHeaderValue,acsOauthScope = getPredixACSConfigfromVcaps()
print("****************** ACS configured As ******************")
print ("\n ACS_URI = " + ACS_URI + "\n "+acsPredixZoneHeaderName+"= " +acsPredixZoneHeaderValue)
print (" ACS zone "+acsOauthScope)
print("****************** ***************** ******************")
createPredixCloudIdentityForMachine()
