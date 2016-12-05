#######################################
# Begin Main script
#######################################
import os
if os.getcwd().endswith("scripts"):
	msg = "Not running from the predix-rmd-ref-app dir.  Please change directory. dir=" + os.getcwd()
	raise ValueError(msg)
	
import sys
import refAppConfig as config
import subprocess
import refApp
import traceback


print ('environment : '+config.environment)
print ('continueFrom=' + config.continueFrom)
print ('only=' + config.only)
print("****************** Installing Reference Application ******************")
try:

	config.retryCount=0
	if config.only not in (''):
		if config.only in ('validate'):
			refApp.validate(config)
		if config.only in ('buildPredixSDKs'):
			refApp.buildPredixSDKs(config)
		if config.only in ('buildReferenceApp'):
			refApp.buildReferenceApp(config)
		if config.only in ('deployReferenceAppDelete'):
			refApp.deployReferenceAppDelete(config)
		if config.only in ('deployReferenceAppCreateUAA'):
			refApp.deployReferenceAppCreateUAA(config)
		if config.only in ('deployReferenceAppCreateACS'):
			refApp.deployReferenceAppCreateACS(config)
			refApp.deployReferenceAppCreateAssetAndTimeseries(config)
			refApp.deployReferenceAppFinalPrep(config)
		if config.only in ('deployReferenceAppCreateAssetAndTimeseries'):
			refApp.deployReferenceAppCreateAssetAndTimeseries(config)
			refApp.deployReferenceAppFinalPrep(config)
		if config.only in ('deployReferenceAppAddAuthorities'):
			refApp.deployReferenceAppAddAuthorities(config)
		if config.only in ('deployReferenceAppCreateDataseed'):
			refApp.deployReferenceAppCreateDataseed(config)
		if config.only in ('deployReferenceAppCreateDatasource'):
			refApp.deployReferenceAppCreateDatasource(config)
		if config.only in ('deployReferenceAppCreateWebsocketServer'):
			refApp.deployReferenceAppCreateWebsocketServer(config)
		#if config.only in ('deployReferenceAppCreateDataIngestion'):
		#	refApp.deployReferenceAppCreateDataIngestion(config)
		if config.only in ('deployReferenceAppCreateDataExchange'):
			refApp.deployReferenceAppCreateDataExchange(config)
		if config.only in ('deployReferenceAppCreateMachineSimulator'):
			refApp.deployReferenceAppCreateMachineSimulator(config)
		if config.only in ('deployReferenceAppCreateUI'):
			refApp.deployReferenceAppCreateUI(config)
		if config.only in ('deployReferenceAppFinalPrep'):
			refApp.deployReferenceAppFinalPrep(config)
		refApp.sanityChecks(config)
	else :
		if config.continueFrom in ('all'):
			#try:
				#refApp.updateGitModules(config)
				refApp.validate(config)
				refApp.buildPredixSDKs(config)
				refApp.buildReferenceApp(config)
				refApp.deployReferenceAppDelete(config)
				refApp.deployReferenceAppCreateUAA(config)
				refApp.deployReferenceAppCreateACS(config)
				refApp.deployReferenceAppCreateAssetAndTimeseries(config)
				refApp.deployReferenceAppAddAuthorities(config)
				refApp.deployReferenceAppCreateDataseed(config)
				refApp.deployReferenceAppCreateDatasource(config)
				refApp.deployReferenceAppCreateWebsocketServer(config)
				#refApp.deployReferenceAppCreateDataIngestion(config)
				refApp.deployReferenceAppCreateDataExchange(config)
				refApp.deployReferenceAppCreateMachineSimulator(config)
				refApp.deployReferenceAppCreateUI(config)
				refApp.deployReferenceAppFinalPrep(config)
				refApp.sanityChecks(config)
			#finally:
				#refApp.restoreGitModules(config)

		if config.continueFrom in ('continue','validate'):
			config.continueFrom = 'continue'
			refApp.validate(config)
		if config.continueFrom in ('continue','buildPredixSDKs'):
			config.continueFrom = 'continue'
			refApp.buildPredixSDKs(config)
		if config.continueFrom in ('continue','buildReferenceApp'):
			config.continueFrom = 'continue'
			refApp.buildReferenceApp(config)
		if config.continueFrom in ('continue','deployReferenceAppDelete'):
			config.continueFrom = 'continue'
			refApp.deployReferenceAppDelete(config)
		if config.continueFrom in ('continue','deployReferenceAppCreateUAA'):
			config.continueFrom = 'continue'
			refApp.deployReferenceAppCreateUAA(config)
		if config.continueFrom in ('continue','deployReferenceAppCreateACS'):
			config.continueFrom = 'continue'
			refApp.deployReferenceAppCreateACS(config)
		if config.continueFrom in ('continue','deployReferenceAppCreateAssetAndTimeseries'):
			config.continueFrom = 'continue'
			refApp.deployReferenceAppCreateAssetAndTimeseries(config)
		if config.continueFrom in ('continue','deployReferenceAppAddAuthorities'):
			config.continueFrom = 'continue'
			refApp.deployReferenceAppAddAuthorities(config)
		if config.continueFrom in ('continue','deployReferenceAppCreateDataseed'):
			config.continueFrom = 'continue'
			refApp.deployReferenceAppCreateDataseed(config)
		if config.continueFrom in ('continue','deployReferenceAppCreateDatasource'):
			config.continueFrom = 'continue'
			refApp.deployReferenceAppCreateDatasource(config)
		if config.continueFrom in ('continue','deployReferenceAppCreateWebsocketServer'):
			config.continueFrom = 'continue'
			refApp.deployReferenceAppCreateWebsocketServer(config)
		if config.continueFrom in ('continue','deployReferenceAppCreateDataExchange'):
			config.continueFrom = 'continue'
			refApp.deployReferenceAppCreateDataExchange(config)
		#if config.continueFrom in ('continue','deployReferenceAppCreateDataIngestion'):
		#	config.continueFrom = 'continue'
		#	refApp.deployReferenceAppCreateDataIngestion(config)
		if config.continueFrom in ('continue','deployReferenceAppCreateMachineSimulator'):
			config.continueFrom = 'continue'
			refApp.deployReferenceAppCreateMachineSimulator(config)
		if config.continueFrom in ('continue','deployReferenceAppCreateUI'):
			config.continueFrom = 'continue'
			refApp.deployReferenceAppCreateUI(config)
		if config.continueFrom in ('continue','deployReferenceAppFinalPrep'):
			config.continueFrom = 'continue'
			refApp.deployReferenceAppFinalPrep(config)

	refApp.sanityChecks(config)

	print("*******************************************")
	print("**************** SUCCESS!! ****************")
	print("*******************************************")
	print ('Visit your live Reference App in the browser: '+ config.uiUrl)
	print ('(Optional) Visit the DataSeedService to load asset data in to the Predix Reference App: '+config.DATA_SEED_URL)
	print ('(Optional) Start the machine data simulator with this command: cf start ' + config.machineSimulatorAppName)
	print ('(Optional) See the accounts and passwords of your ref app at the bottom of the file scripts/refAppConfig.py')
except:
	print()
	print(traceback.print_exc())
	print()
	if config.only in (''):
		print ('Exception when running ' + config.current + '.  After repairing the problem, use "--continueFrom ' + config.current + '" switch to resume the install')
	print
	sys.exit(2)
