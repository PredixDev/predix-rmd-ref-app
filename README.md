<a href="http://predixdev.github.io/predix-rmd-ref-app" target="_blank">
	<img height="50px" width="100px" src="https://github.com/PredixDev/predix-rmd-ref-app/blob/master/images/pages.jpg?raw=true" alt="view github pages">
</a>

Predix RMD Reference App 
=====================

Welcome to the Predix Remote Monitoring & Diagnostics (RMD) Reference Application.  The Predix platform enables you to create applications with an Industrial Internet focus and allows you to manage and scale those applications as they are consumed by your end users.  

The RMD Reference App shows developers and architects how to use and leverage all of the Predix application building block Services you find in the <a href="https://www.predix.io/catalog" target="_blank">Catalog</a>.  So, it only has some aspects of a fully featured RMD application.  Instead, it's intent is to show developers and architects a best-practices microservices application architecture integrating with all the underlying Predix Services.  It will save you a few weeks or months of effort if you leverage the components inside.    

You can view a running version of the  [Reference App](https://rmd-ref-app.run.aws-usw02-pr.ice.predix.io/dashboard) in your browser using these login credentials

        User: app_user_1
        Password: App_User_111
        
You can view our <a href=https://youtu.be/2MGPTJ8yjyc target="_blank">Video</a> and later run the [deployment script ](https://www.predix.io/resources/tutorials/tutorial-details.html?tutorial_id=2106&tag=1610&journey=Digital%20Twin%3A%20from%20the%20Edge%20to%20the%20Cloud%20using%20RMD%20Reference%20App&resources=1592,1473,2106,1600), which will push the Reference App to your own Cloud Foundry space so you can quickly start trying out various Predix Services.

Now, take a few moments to learn all about  Predix, using Reference App as a guide.  There is lots to discover and soon you'll be creating Predix Apps of your own.

## Predix Integration
The Reference App Front-End and Back-End Microservices demonstrate how to use the Predix PAAS to build an Industrial Internet application.  The app takes advantage of the following Predix components:

[Base Asset Monitoring Reference App Installer](https://www.predix.io/resources/tutorials/tutorial-details.html?tutorial_id=2106&tag=1610&journey=Digital%20Twin%3A%20from%20the%20Edge%20to%20the%20Cloud%20using%20RMD%20Reference%20App&resources=1592,1473,2106,1600)
- [Predix WebApp Starter](https://github.com/predixdev/predix-webapp-starter)
- [Predix UAA Security](https://docs.predix.io/en-US/content/service/security/user_account_and_authentication/)
- [Predix Asset](https://docs.predix.io/en-US/content/service/data_management/asset/)
- [Predix Time Series](https://docs.predix.io/en-US/content/service/data_management/time_series/)

[Digital Twin Analytics Reference App Installer](https://www.predix.io/resources/tutorials/journey.html#1611)
- [Predix Analytics](https://docs.predix.io/en-US/content/service/analytics_services/analytics_framework/)

[Edge Starters - Personal Edition Installer](https://www.predix.io/resources/tutorials/journey.html#2054)
- [Predix Machine](https://docs.predix.io/en-US/content/service/edge_software_and_services/machine/)
- [Predix Machine Modbus Adapter](https://docs.predix.io/en-US/content/service/edge_software_and_services/machine/modbus-machine-adapter)
- [Predix Data River Receiver](https://docs.predix.io/en-US/content/service/edge_software_and_services/machine/data-bus-river#concept_7975e96d-33fc-4cba-811a-8dc895d98f94)

## RMD Reference App
RMD Reference App is composable and the pieces can be used in a variety of configurations to help solve your Application use-case.  Like most Apps, at it's core, Reference App consists of a [RMD UI](#microservices) front end microservice and a [RMD Datasource](#microservices) back-end microservice.   

<img src="https://github.com/PredixDev/predix-rmd-ref-app/blob/master/images/RefApp-CoreMicroservices.png?raw=true">

Beyond the core services there are other [microservices](#microservices) and [microcomponent utilities](#microcomponents) which help generate Data, make Secure Rest calls or integrate with all the different Predix Services and Security.

## Detailed Architecture of the Base Asset Monitoring Reference App

Architecturally the reference app is organized into four Tiers (Presentation, Delivery, Aggregation and Storage) and supports three Data Flows (Ingestion, Analytics, Visualization)
- Presentation Tier - UI layer and microservices
- Delivery Tier - Cacheing, Mobile, Personalization
- Aggregation Tier - Service Composition and Business Logic
- Storage Tier - the Predix PAAS Services

<img src="https://github.com/PredixDev/predix-rmd-ref-app/blob/master/images/refapp_arch1.png?raw=true" width="600px">

The 2 main microservices and some helper microservices which are pushed to and run in cloud foundry, as follows:

<img src="https://github.com/PredixDev/predix-rmd-ref-app/blob/master/images/ReferenceApp-Microservices3.png?raw=true" width="600px">

### Ingestion Flow
In your production Edge to Cloud architecture, Predix Machine using the Predix Machine DataRiver posts data over a websocket to the Time Series service directly.  To get a feel for this, our companion Edge Starter reference applications (links shown above) show how to configure that.  

With the Base Reference App however, the Predix Machine is not installed by the install script.  Instead we install a microservice called the Data Exchange Simulator.  Data Flows from the Data Exchange Simulator to the Data Exchange and on to Predix Time Series.  The Data Exchange also acts as a websocket server, which feeds live data to the RMD Reference App UI in near real-time.

(future) Raw data often needs cleaning and preparation before it is consumable via Analytics and UI.  A best-practice would be to mark this data as raw and trigger Cleansing and Quality jobs leveraging the analytics framework.  

<img src='https://github.com/PredixDev/predix-rmd-ref-app/blob/master/images/RefApp-IngestionFlow3.png?raw=true' >

### Ingestion Flow (pipeline architecture)
(future) For many applications, there is a need to be in the flow of data as it arrives.  The Event Hub service provides a subscription mechanism as the data comes in, the proposed flow below has data coming in to the Data Exchange so that other actions can be taken.  Examples are:

- Sending data to the Web Socket Clients, so data streams directly to the UI
- Putting a message on a Queue to trigger downstream processes
- Enriching or Filtering the data in a Custom Handler

We leave these enhancements to you to implement depending on your application use-case.

<img src='https://github.com/PredixDev/predix-rmd-ref-app/blob/master/images/RefApp-IngestionFlow-pipeline.png?raw=true' >


### Visualization Flow
The UI accesses data from Predix Asset directly which drives the Asset selector menu. Once a selection is made the View requests data from the RMD Datasource and returns the data from Predix Asset and Predix Time Series in a mashup.  However, in the Graph Widget the Time Series service is accessed directly. 

<img src='https://github.com/PredixDev/predix-rmd-ref-app/blob/master/images/RefApp-VisualizationFlow.png?raw=true' width=600 height=400>

## Detailed Architecture of the Digital Twin Analytics Reference App

Since we have your attention, we'd like to introduce the features of our Digital Twin Analytics Reference App.  This builds on the base Reference App to add the ability to trigger analytic processes.  The DT Analytics Reference App uses a separate installer (see links above).

### Analytics Flow		
Data arrives via the Ingestion Flow and is stored.  A message is placed in a queue which kicks off an Analytic Orchestration.  The Analytics uses data from Predix Asset and Predix Time Series, produces a result, which is then stored back to Predix Asset or Predix Time Series or potentially to/from any other datastore.		
		
<img src='https://github.com/PredixDev/predix-rmd-ref-app/blob/master/images/RefApp-AnalyticsFlow2.png?raw=true' >		

## Getting Acquainted with Reference App

Go through the following Guide to get acquainted with Predix RMD Reference application.

[Digital Twin: from the Edge to the Cloud using RMD Reference App](https://www.predix.io/resources/tutorials/journey.html#1610)


## Setting up your environment
Reference App accesses code repos at https://github.com/PredixDev and a maven repository at https://artifactory.predix.io.

The best experience is to use a [DevBox](https://www.predix.io/services/other-resources/devbox.html) which has all the tools and settings pre-installed.  

Use the quickstart script [in the tutorial](https://www.predix.io/resources/tutorials/journey.html#1610) to install the tools and the app.  

For more detailed instructions on tools installationn, follow the link below to setup your development environment:

[Development Environment](https://www.predix.io/resources/tutorials/journey.html#1607)


## Predix Hello World
Go through the following tutorial on how to build a simple hello world application using Predix components.

[Hello World](https://www.predix.io/resources/tutorials/journey.html#1719)


## Microservices
The base Asset Monitoring Ref App consists of 2 core microservices and 3 helper microservices. Each microservice can be individually managed and scaled, leveraging the Cloud Foundry infrastructure. These services can be mixed and matched for your next Predix application depending on which services you need to integrate with.

### [RMD Ref App UI](https://github.com/PredixDev/predix-webapp-starter/blob/master/public/docs/ABOUT.md)
A Polymer Web Components based UI framework. We started with the [Polymer Webapp Starter](https://github.com/PredixDev/predix-webapp-starter) for UI Development which comes with a JSON only mode that is not hooked to back-end Predix services.   The very same github repo serves as the RMD Reference App UI and is instrumented with best-practice behaviors for hooking to real back-end Predix services and apps.   The UI talks to the RMD Datasource Service, Predix UAA, Predix Asset and Predix Timerseries back-end services.

More details can be found [here](https://github.com/PredixDev/predix-webapp-starter/blob/develop/public/docs/ABOUT.md).

### [RMD Datasource Service](https://github.com/PredixDev/rmd-datasource/blob/master/README.md#welcome-to-the-rmd-datasource-microservice)
A Mashup Service doing much of the logic for the Reference App.  It talks to Predix Asset and Time Series databases and return results for display.

### [DataExchange](https://github.com/predixdev/data-exchange/tree/master#data-exchange)
  The DataExchange framework retrieves data from any Datasource using a simple Get or Put API.  Inside the Data Exchange are handlers for Asset, Timeseries, RabbitMQ, and WebSockets.  An empty CustomHandler is provided so you can hook to your custom datasource (e.g. Postgres). DataExchange can help manage data Get/Put requests that are from distributed, near-data, relational db, public internet, file dataources, via other Rest APIs and also can be used at the Edge (on Machines outside the cloud).  The Data Exchange can also act as a websocket server, to broadcast data to clients over websockets.

### [Data Exchange Simulator Service](https://github.com/PredixDev/data-exchange-simulator/tree/master)
  A Service to generate time series data when a physical machine is not available.  The Simulator sends data to the Data Exchange Service.  The install script lets the simulator run for 30 seconds and then stops it.  This is so data is not unnecessarily flowing in to Predix Time Series.

## Asset Model

Using the tutorial below, you will learn about the RMD Reference App asset model to help understand how you can create your own asset model for your Industrial Assets.

[Reference App and Predix Asset](https://www.predix.io/resources/tutorials/journey.html#1709)

## APIs
The reference app defines some apis and message bodies that are needed to communicate between microservices.  They are defined by xsd but at runtime use JSON.
* [RMD Datasource](https://github.com/PredixDev/rmd-datasource)
* [Run Analytic](https://github.com/PredixDev/ext-interface/blob/master/ext-model/src/main/resources/META-INF/schemas/predix/entity/runanalytic/runanalytic.xsd)
* [Data Exchange - GetFieldData](https://github.com/PredixDev/ext-interface/blob/3279197f26802afd3c4eb5d181390313868caa9f/ext-model/src/main/resources/META-INF/schemas/predix/entity/getfielddata/getfielddata.xsd)
* [Data Exchange - PutFieldData](https://github.com/PredixDev/ext-interface/blob/3279197f26802afd3c4eb5d181390313868caa9f/ext-model/src/main/resources/META-INF/schemas/predix/entity/putfielddata/putfielddata.xsd)
* [FieldChangedEvent](https://github.com/PredixDev/ext-interface/blob/master/ext-model/src/main/resources/META-INF/schemas/predix/event/fieldchangedevent/fieldchangedevent.xsd)

## Microcomponents
* [Predix Microcomponent Bootstraps](docs/microcomponents.md) - reusable libraries that can be used in any microservice
 
## SDKs
One of the primary points of the Reference App is to provide sample code and SDKs that help you talk to real Predix Services.  [We have SDKs](https://www.predix.io/resources/tutorials/journey.html#SDK) for many of the services in several languages including for UAA, Asset, Timeseries, Analytic Runtime, basic REST client, basic WebSocket client, etc.


#### Known Issues
* Safari has visual issues

### More Details
* [RMD overview](https://github.com/predixdev/predix-rmd-ref-app/tree/master/docs/overview.md) - the Remote Monitoring & Diagnostics use-case
* [Securing an application](https://github.com/predixdev/predix-rmd-ref-app/tree/master/docs/security.md)
* [More GE resources](https://github.com/predixdev/predix-rmd-ref-app/tree/master/docs/resources.md)

[![Analytics](https://predix-beacon.appspot.com/UA-82773213-1/predix-rmd-ref-app/readme?pixel)](https://github.com/PredixDev)
