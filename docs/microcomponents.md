##Microcomponents

Microcomponents are reusable libraries that can be used in any microservice.  The Adoption team has developed many Bootstrap Microcomponents, the following are relevent to the current version of Predix.

- [Predix Microservice Templates](#PredixMicroserviceTemplates)
- [Predix Rest Client](#PredixRestClient)
- [Predix Rest Client](#PredixWebSocketClient)
- [Asset Bootstrap Client](#AssetBootstrapClient)
- [Timeseries Bootstrap Client](#TimeseriesBootstrapClient)

###<a name="PredixMicroserviceTemplates" href="https://github.com/predixdev/predix-microservice-templates">PredixMicroserviceTemplates</a>
A collection of back-end Microservice bootstraps that gets you creating a Microservice much quicker than starting from scratch.  For Java, we started with SpringBoot helloWorld and added CXF, Tomcat, Spring Profiles and Property File management features that you would need anyway.  Other templates for NodeJS, etc are on their way.

###<a name="PredixRestClient" href="https://github.com/predixdev/predix-rest-client">Predix Rest Client</a>
Predix Rest Client has GET, PUT, POST, DELETE calls that integrate with Predix UAA Security.  Everything is property-ized from the Hostname to Port to Proxy server urls to JWT vs SAML token support.  It works backwards compatible to Predix 1.0 security as well so you can use it port services from Predix 1.0 to 2.0 in the cloud.

###<a name="PredixWebSocketClient" href="https://github.com/predixdev/predix-websocket-client">Predix WebSocket Client</a>
Coming Soon.  Predix Web Socket Client has WebSocket OPEN, CLOSE, SEND, RECEIVE calls that integrate with Predix UAA Security.  Everything is property-ized from the Hostname to Port to Proxy server urls to JWT token support.

###<a name="AssetBootstrapClient" href="https://github.com/predixdev/asset-bootstrap">Asset Bootstrap Client</a>
Asset Bootstrap exposes the Predix Asset APIs for Groups, Classifications, Assets and Meters.  It also provides the ability to pass through or get tokens from Predix UAA Security.  This is also backwards compatible, at this time, to Predix Asset 14.3.

###<a name="TimeseriesBootstrapClient" href="https://github.com/predixdev/timeseries-bootstrap">Timeseries Bootstrap Client</a>
Timeseries Bootstrap exposes the Predix Timeseries APIs.  Support for Start/End Date based timeseries calls are much more easily exposed including support for Predix UAA calls to Security Authorization.

