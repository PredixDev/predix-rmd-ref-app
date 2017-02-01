## Developing and Configuring Microservices

### Predix Components

#### Asset Service 
This service is available through service broker and provided in the cloud foundry. For the RMD application, the asset service instance can be created, if the instance is not already present in the space. The RMD application is configured for the "predixAsset" service instance name.
```
cf create-service stc-asset beta-plan predixAsset
```

####  Timeseries Service
This service is available through service broker and provided in the cloud foundry. For the RMD application, the timeseries service instance can be created, if the instance is not already present in the space. 


To deploy:
+ cd to the clone directory
+ cf push 

##### Ingesting Timeseries data


There are two ways to insert data into the time series DB.
1. To automatically generate some random data and insert into Timeseries, scripts are provided here: <https://github.sw.ge.com/predix-integration/rmd-ui-service/tree/develop/data-scripts/timeseries-data>. Follow README instructions in this folder.  Modify generate-data.sh script update tag names, so you don't overwrite data for tags others are using.  Tag names could be tied to the "sourceTagId" field in Predix Asset, to associate time-series data with an asset.
2. Use the Predix Machine services described below.  This way, you can either ingest real data from a device, or ingest sample data from a simulator.

####  Predix Authentication Service UAA based configuration.
The application is configured with Predix UAA configuration. The client application id is configured on the UAA for this application. 
Login: app_user_1 / app_user_1

***

### Customized RMD application specific Microservices

#### Dashboard View Service
- This service is repository for the views displayed by the px-contextual-dashboard.  Each view is associated with an asset classification.
- You can create an instance of the views service by following the steps described here, in the [seed application View Service setup.](https://github.com/PredixDev/predix-seed/tree/1.0#binding-to-view-service).
- Alternatively, you can create your own views service that returns JSON in the correct format.  You could modify and deploy the [rmd-ui-service](https://github.com/PredixDev/rmd-ui-service/tree/develop) described below.
- Run the views script documented below to register the views configured for the RMD application.

#### Application meta-context Service
This service is repository that holds application datasource meta-context.  Widgets used in the Predix Dashboard call this service to find datasources.

To deploy:
+ git clone https://github.sw.ge.com/predix-integration/rmd-ui-service/tree/develop ( branch)
+ cd to the clone directory
+ modify manifest.yml and give the application a unique name.
+ mvn clean install
+ cf push 
- verify the service is deployed calling the {application_url}/views and setting the Authorized token. 

####  Experience Datasource bootstrap Service  
This service has orchestration , that provides data to data-grids and widgets.  Github repo for this service is located here: <https://github.sw.ge.com/adoption/experience-datasource-bootstrap>  This bootstrap is dependent on the following micro component dependencies uploaded to the artifactory.
1. (predix-rest-client) https://github.com/PredixDev/predix-rest-client
2. (asset-bootstrap-client) https://github.sw.ge.com/adoption/asset-bootstrap.git 
3. (timeseries-bootstrap-client)  https://github.sw.ge.com/adoption/timeseries-bootstrap.git (develop)

To deploy:
+ git clone https://github.sw.ge.com/adoption/experience-datasource-bootstrap.git
+ cd <<clone directory>> 
+ mvn clean install  
+ cd <datasource-service> 
+ cf push 

### Data Seed Service
This service was used to construct and populate the asset model.  You can create a datamodel in an Excel spreadsheet, then  upload to this service.  The service will make the correct Predix Asset REST API calls to create or update the model.

<https://github.com/PredixDev/data-seed-service>

A sample excel spreadsheet can be found here, in the AssetData.xls file: <https://github.com/PredixDev/data-seed-service/tree/master/dataseed-service/src/main/resources/rmdapp>

### Predix Machine Services
This repo contains bundles to run in Predix Machine, as well as an ingestion service to store data in the time series DB.

<https://github.com/PredixDev/RMDReferenceApp> 

### ADH-PAPI Service - https://github.sw.ge.com/adoption/adh-papi
 - implements the ADH API and retrieves Asset data

### ADH-Router Service - https://github.sw.ge.com/adoption/adh-router-service
 - implements the ADH API and routes requests to the appropriate ADH Handler or Microservice
