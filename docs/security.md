## Securing the Application

### Authentication 

Predix Authentication service (UAA) is configured for this application.  In practice, you'd probably want to federate with GE SSO. In order to enable your application to have a GE SSO, please work with Predix security team.This service is available through service broker and provided in the cloud foundry .For the RMD application , the security service can be created .The RMD application is configured for the "rmd_uaa_%username%" service instance name .The %username% is the cf login username. 

```
cf cs predix-uaa beta rmd_uaa_%username% -c '{"adminClientSecret": "secret"}'
```
Once the instance of the predix-uaa is generated. Install the uaac tool (follow the Security service documentation for setting up the uaac and details on setting on the client ) . 

Once you get the applicationId (aka clientId), go to your appliction frontend project (see rmd-predix-ui project), specify your clientId in /public/scripts/app.js:

	$scope.clientId = 'your_client_id';

### Authorization

Predix ACS service can provide role based authorization for your application. Please refer to Predix ACS service documentation to use this feature: <https://github.com/predix/acs>  Role based authorization was not implemented for this RMD reference app.
