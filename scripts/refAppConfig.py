import os
import subprocess
import sys, getopt
import re

def checkRequirements():
    try:
        cfTarget = subprocess.check_output(["cf", "target"])
        print (cfTarget)
        user = cfTarget.decode('utf8').split('User:')[1].split('Org:')[0]
        org = cfTarget.decode('utf8').split('Org:')[1].split('Space:')[0]
        space = cfTarget.decode('utf8').split('Space')[1]
        print("cf login detected")
        return (user.strip(), org, space)
    except subprocess.CalledProcessError as e:
        sys.exit("Please login to Predix.")

#global org
#global space
#global user
global instanceAppender
global BASE_DIR
global BASE_PREDIX_DIR
global rmdUaaName
global rmdAcsName
global rmdPredixAssetName
global rmdPredixTimeseriesName
global rmdPostgres
global rmdRedis
global predixbootAppName
global dataSeedAppName
global dataSourceAppName
#global httpDataRiverAppName
global dataExchangeAppName
global dataIngestionAppName
global machineSimulatorAppName
global dataExchangeSimulatorAppName
global uiAppName
global websocketAppName
global fdhAppName
global rmdRabbitMQ
global predixUaaService
global predixAcsService
global predixAssetService
global predixTimeSeriesService
global predixPostgres
global predixRedis
global predixRabbitMQ
global predixUaaServicePlan
global predixAcsServicePlan
global predixAssetServicePlan
global predixTimeSeriesServicePlan
global predixPostgresPlan
global predixRedisPlan
global predixRabbitMQPlan
global rmdAppClientId
global rmdAppSecret
global uaaAdminSecret
global clientAuthorities
global clientScope
global projectDir
global predixProject
global rmdUser1
global rmdUser1Pass
global deleteAppsAndServices
global environment
global mvnsettings
global pullsubmodules
global mavenRepo
global continueFrom
global artifactoryrepo
global artifactoryuser
global artifactorypass
global resolver
global user

try:
    #set defaults
    instanceAppender = ""
    #mvnsettings = "~/.m2/settings.xml"
    from os.path import expanduser
    homeDir = expanduser("~")

    mvnsettings=os.path.join(homeDir, ".m2", "settings.xml")

    #mvnsettings = ""
    pullsubmodules = 'y'
    mavenRepo = ""
    deleteAppsAndServices = "n"
    environment = "PROD"
    continueFrom = "all"
    only = ""
    fastinstall = 'y'
    artifactoryrepo = ""
    artifactoryuser = ""
    artifactorypass = ""
    resolver = "10.72.0.2"
    #override with arguments
    opts, args = getopt.getopt(sys.argv[1:],"d:e:i:s:p:r:a:v:c:o:f:x:y:z:",["delete=","environment=","instanceAppender=","mvnsettings=","pullsubmodules=","mavenrepo=","continueFrom=","only=", "fastinstall=", "artifactoryrepo=", "artifactoryuser=", "artifactorypass="])
except getopt.GetoptError:
    print('Exception when parsing : '+sys.argv[0]+' -e (R2/PROD) -i <Instance appender> -s <mvnsettings>')
    sys.exit(2)
for opt, arg in opts:
    print ('opt=' + opt + ' arg=' + arg)
    if opt == '-h':
        print(sys.argv[0]+' -e (R2/PROD) -g <Github User> -i <Instance appender> -s <Maven settings file>')
        sys.exit()
    elif opt in ("-i", "--instanceappender"):
        instanceAppender = arg
    elif opt in ("-d", "--delete"):
        deleteAppsAndServices = arg
    elif opt in ("-e", "--environment"):
        environment = arg
    elif opt in ("-s", "--mvnsettings"):
        mvnsettings = arg
    elif opt in ("-p","--pullsubmodules"):
        pullsubmodules = arg
    elif opt in ("-r","--mavenrepo"):
        mavenRepo = arg
    elif opt in ("-v","--verbose"):
        verbose = true;
    elif opt in ("-c","--continueFrom"):
        continueFrom = arg;
    elif opt in ("-o","--only"):
        only = arg;
    elif opt in ("-f","--fastinstall"):
        fastinstall = arg;
    elif opt in ("-x","--artifactoryrepo"):
        artifactoryrepo = arg;
    elif opt in ("-y","--artifactoryuser"):
        artifactoryuser = arg;
    elif opt in ("-z","--artifactorypass"):
        artifactorypass = arg;

#if mvnsettings == "":
#        print sys.argv[0]+' -e (R2/PROD) -g <Github User> -i <Instance appender> -s <Maven settings file>'
#        print 'Maven settings file is a mandatory argument.'
#        sys.exit()

# check check login
user, org, space = checkRequirements()
if len(instanceAppender) == 0:
    instanceAppender = user.strip().split("@")[0].replace('.', '_')
print ('using Appender', instanceAppender)

# check or create a directory for Reference application
BASE_DIR = os.getcwd()
BASE_PREDIX_DIR = "PredixApps"

# Reference App Service Instance Names
rmdUaaName = instanceAppender+"-uaa"
rmdAcsName = instanceAppender+"-acs"
rmdPredixAssetName = instanceAppender+"-asset"
rmdPredixTimeseriesName = instanceAppender+"-time-series"
rmdPostgres = instanceAppender+"-postgres"
rmdRedis = instanceAppender+"-redis"


predixbootRepoName="Predix-HelloWorld-WebApp"
predixSDKs="predix-sdks"

# Predix Application Names
print ('instanceAppender=' + instanceAppender)

predixbootAppName = instanceAppender+"-hello-world"
dataSeedAppName = instanceAppender+"-data-seed"
dataSourceAppName = instanceAppender+"-rmd-datasource"
httpDataRiverAppName = instanceAppender+"-http-datariver"
dataIngestionAppName = instanceAppender+"-dataingestion"
dataExchangeAppName = instanceAppender+"-data-exchange"
machineSimulatorAppName = instanceAppender+"-machinedata-simulator"
dataExchangeSimulatorAppName = instanceAppender+"-data-exchange-simulator"
uiAppName = instanceAppender+"-rmd-ref-app-ui"
websocketAppName = instanceAppender+"-websocket-server"
fdhAppName = instanceAppender+"-fdh-router-service"
rmdRabbitMQ= instanceAppender+"-rabbitmq"
if environment == 'PROD' or environment == 'SELECT':
    # Predix Service Instance Name for VPC
    predixUaaService = "predix-uaa"
    predixAcsService = "predix-acs"
    predixAssetService = "predix-asset"
    predixTimeSeriesService = "predix-timeseries"
    predixPostgres = "postgres"
    predixRedis = "redis"
    predixRabbitMQ = "rabbitmq-36"

    predixUaaServicePlan = "Free"
    predixAcsServicePlan = "Free"
    predixAssetServicePlan = "Free"
    predixTimeSeriesServicePlan = "Free"
    predixPostgresPlan = "shared"
    predixRedisPlan = "shared-vm"
    predixRabbitMQPlan = "standard"
    artifactoryrepo = "https://artifactory.predix.io/artifactory/PREDIX-EXT"
elif environment == 'FREE' :
    # Predix Service Instance Name for sysint
    predixUaaService = "predix-uaa"
    predixAcsService = "predix-acs"
    predixAssetService = "predix-asset-sysint"
    predixTimeSeriesService = "predix-timeseries-sysint"
    predixPostgres = "rdpg"
    predixRedis = "p-redis"
    predixRabbitMQ = "rabbitmq-36"

    predixUaaServicePlan = "free"
    predixAcsServicePlan = "Free"
    predixAssetServicePlan = "Beta"
    predixTimeSeriesServicePlan = "Beta"
    predixPostgresPlan = "shared-nr"
    predixRabbitMQPlan = "standard"
    predixRedisPlan = "shared-vm"
else :
    # Predix Service Instance Name for sysint
    predixUaaService = "predix-uaa-sysint"
    predixAcsService = "predix-acs-sysint"
    predixAssetService = "predix-asset-sysint"
    predixTimeSeriesService = "predix-timeseries-sysint"
    predixPostgres = "rdpg"
    predixRedis = "p-redis"
    predixRabbitMQ = "rabbitmq-36"

    predixUaaServicePlan = "free"
    predixAcsServicePlan = "free"
    predixAssetServicePlan = "Beta"
    predixTimeSeriesServicePlan = "Beta"
    predixPostgresPlan = "Free"
    predixRabbitMQPlan = "standard"
    predixRedisPlan = "shared-vm"

if environment == 'SELECT':
    resolver = "10.128.99.10"
    predixRedis = "redis-1"

#Reference application client id
rmdAppClientId = "app_client_id"
rmdAppSecret = "secret"
#UAA Admin Account
uaaAdminSecret = "secret"
clientGrantType = ["authorization_code","client_credentials","refresh_token","password"]
clientAuthorities = ["openid","acs.policies.read","acs.policies.write","acs.attributes.read","acs.attributes.write","uaa.resource","uaa.none"]
clientScope = ["uaa.none","openid","acs.policies.read","acs.policies.write","acs.attributes.read","acs.attributes.write"]

projectDir = "predix-microservice-templates"
predixProject = projectDir+".git"
#UAA User account for logging in to RMD Ref App
rmdUser1 = "app_user_1"
rmdUser1Pass = "app_user_1"
#Admin User that is allowed to add asset data
rmdAdmin1 = "app_admin_1"
rmdAdmin1Pass = "app_admin_1"
acsPolicyName= "refapp-acs-policy"
