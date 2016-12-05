## Pulling Submodules and Manual Steps

This page will be a work-in-progress for a while till we get every last step documented.

1. Download and build
  2. Run ./pullSubmodules.sh to download all the Git submodule repositories
  1. Run mvn clean package
    * do not run, mvn clean install, which runs integration tests that won't match up to your org/space yet
    * after you have run the install python script, you can update with your client id:secret and instance names 
1. Push [Predix-Microservice-Templates](https://github.com/PredixDev/predix-rmd-ref-app/blob/master/docs/microcomponents.md#PredixMicroserviceTemplate) to have something to bind to
1. Create Secure Client Id and User
  1. Create UAA defining an Admin secret
      * <code> cf cs predix-uaa beta ${UAA_INSTANCE_NAME} -c '{"adminClientSecret":"${UAA_ADMIN_SECRET}"}' </code>
  2. Bind predix-microservice-cf-jsr311 to UAA
      * <code> cf push predix_boot_cf_${APP_NAME} -f <BASE_DIR>/predix-boot/predix-boot-cf/manifest.yml </code>
      * <code> cf bind-service predix_boot_cf_${APP_NAME} ${UAA_INSTANCE_NAME} </code> 
  3. View VCAP to get UAA Instance Id and URL
     * <code> cf env predix_boot_cf_${APP_NAME}</code>
      ```
    *** SAMPLE Response ****
      VCAP_SERVICES {
      "predix-uaa": [
                 {
                  "credentials": {
                   "issuerId": "https://86458c66-5e75-43d3-892a-9d37c2b67cb2.predix-uaa.run.aws-usw02-pr.ice.predix.io/oauth/token",
                   "uri": "https://86458c66-5e75-43d3-892a-9d37c2b67cb2.predix-uaa.run.aws-usw02-pr.ice.predix.io",
                   "zone": {
                    "http-header-name": "X-Identity-Zone-Id",
                    "http-header-value": "86458c66-5e75-43d3-892a-9d37c2b67cb2"
                   }
                  },
                  "label": "predix-uaa",
                  "name": "rmd_uaa_test",
                  "plan": "beta",
                  "tags": []
                 }
                ]
      }
      ```
  4. Create Asset using UAA as trustedIssuer
      * <code>cf cs predix-asset beta ${ASSET_INSTANCE_NAME} -c '{"trustedIssuerIds":["${UAA_VCAPS_ISSUERID}"]}'</code>
  5. Create Timeseries using UAA as trustedIssurer
      * <code>cf cs predix-timeseries beta ${TS_INSTANCE_NAME} -c '{"trustedIssuerIds":["${UAA_VCAPS_ISSUERID}"]}' </code> 
  6. Create ACS using UAA as trustedIssuer
      * <code>cf cs predix-acs beta ${ACS_INSTANCE_NAME} -c '{"trustedIssuerIds":"${UAA_VCAPS_ISSUERID}"}' </code> 
  7. Bind Asset, Timeseries,ACS to Predix-Boot
      1. <code>cf bind-service predix_boot_cf_${APP_NAME} ${ASSET_INSTANCE_NAME}</code>
      2. <code>cf bind-service predix_boot_cf_${APP_NAME} ${TS_INSTANCE_NAME}</code>
      3. <code>cf bind-service predix_boot_cf_${APP_NAME} ${ACS_INSTANCE_NAME}</code> 
  8. View UAA to get instance ids
      *<code>cf env predix_boot_cf_${APP_NAME}</code>
  9. Set UAAC target to uaa instance
      *<code>cf env predix_boot_cf_${APP_NAME}</code>
  10. Become UAAC admin user
      1. *<code>uaac target ${UAA_VCAPS_ISSUERID}</code>
      2. *<code>uaac token client get admin -s ${UAA_ADMIN_SECRET}</code>
  11. Create Client Id 
     1. *<code>uaac client add ${CLIENT_ID} -s ${CLIENT_SECRET} --authorized_grant_types "authorization_code client_credentials refresh_token password" --autoapprove openid --authorities "openid acs.policies.read acs.policies.write acs.attributes.read acs.attributes.write uaa.resource uaa.none" --scope "uaa.none openid,acs.policies.read acs.policies.write acs.attributes.read acs.attributes.write"</code>
  12. Create User
      1. <code> uaac user add app_user_1 -p app_user_1 --email rmd@user-test.com </code>
      2. <code> uaac user add app_admin_1 -p app_admin_1 --email rmd@admin-test.com</code>
  13. Create Groups using scope names from Asset, Timeseries and ACS
      Get Asset,Timeseries and ACS scopes **(predix-acs.zones,timeseries.zones,predix-asset.zones)** from VCAPS from Step 9.
    ```  
    uaac client update ${CLIENT_ID} --authorities "acs.policies.read acs.policies.write predix-acs.zones.1341441c-8fdf-4b53-85d6-b93d056580e6.user uaa.resource timeseries.zones.279e71e0-1dd8-4a64-86b1-09a8b5e8b02b.user acs.attributes.read predix-asset.zones.24d6aadd-f13e-4d20-849e-a8544f978d8d.user openid uaa.none timeseries.zones.279e71e0-1dd8-4a64-86b1-09a8b5e8b02b.query acs.attributes.write timeseries.zones.279e71e0-1dd8-4a64-86b1-09a8b5e8b02b.ingest" --scope "acs.policies.read acs.policies.write predix-acs.zones.1341441c-8fdf-4b53-85d6-b93d056580e6.user uaa.resource timeseries.zones.279e71e0-1dd8-4a64-86b1-09a8b5e8b02b.user acs.attributes.read predix-asset.zones.24d6aadd-f13e-4d20-849e-a8544f978d8d.user openid uaa.none timeseries.zones.279e71e0-1dd8-4a64-86b1-09a8b5e8b02b.query acs.attributes.write timeseries.zones.279e71e0-1dd8-4a64-86b1-09a8b5e8b02b.ingest"
      ```
  14. Add User to Groups
    For the scopes for **(predix-acs.zones,timeseries.zones,predix-asset.zones)** from VCAPS from Step 9
    1. Check if the group on the UAA exist
        1. *<code>uaac group get predix-acs.zones.1341441c-8fdf-4b53-85d6-b93d056580e6.user </code>
        2. *<code>uaac group get timeseries.zones.279e71e0-1dd8-4a64-86b1-09a8b5e8b02b.user </code>
        3. *<code>uaac group get predix-asset.zones.24d6aadd-f13e-4d20-849e-a8544f978d8d.user </code>
        4. *<code>uaac group get timeseries.zones.279e71e0-1dd8-4a64-86b1-09a8b5e8b02b.query </code>
        5. *<code>uaac group get acs.policies.read </code>
        6. *<code>uaac group get aacs.policies.write </code>
        7. *<code>uaac group get acs.attributes.read </code>
        8. *<code>uaac group get acs.attributes.write </code>
  2. If group does not exist - create a group
      1. *<code>uaac group add predix-acs.zones.1341441c-8fdf-4b53-85d6-b93d056580e6.user </code>
      2. *<code>uaac group add timeseries.zones.279e71e0-1dd8-4a64-86b1-09a8b5e8b02b.user </code>
      3. *<code>uaac group add predix-asset.zones.24d6aadd-f13e-4d20-849e-a8544f978d8d.user </code>
      4. *<code>uaac group add timeseries.zones.279e71e0-1dd8-4a64-86b1-09a8b5e8b02b.query </code> 
      5. *<code>uaac group add acs.policies.read </code>
      6. *<code>uaac group add aacs.policies.write </code>
      7. *<code>uaac group add acs.attributes.read </code>
      8. *<code>uaac group add acs.attributes.write </code>
  3. Add users created on Step 12  to the Group 
      1. *<code>uaac member add predix-acs.zones.1341441c-8fdf-4b53-85d6-b93d056580e6.user app_user_1</code>
      2. *<code>uaac member add timeseries.zones.279e71e0-1dd8-4a64-86b1-09a8b5e8b02b.user app_user_1</code>
      3. *<code>uaac member add predix-asset.zones.24d6aadd-f13e-4d20-849e-a8544f978d8d.user app_user_1</code>
      4. *<code>uaac member add timeseries.zones.279e71e0-1dd8-4a64-86b1-09a8b5e8b02b.query app_user_1</code> 
      5. *<code>uaac member add predix-asset.zones.24d6aadd-f13e-4d20-849e-a8544f978d8d.user app_user_1</code>
      6. *<code>uaac member add timeseries.zones.279e71e0-1dd8-4a64-86b1-09a8b5e8b02b.query app_user_1</code> 
      7. *<code>uaac member add acs.policies.read app_user_1</code>
      8. *<code>uaac member add acs.attributes.read app_user_1</code> 
      
For Policy Admin user
      1. *<code>uaac member add acs.policies.read app_admin_1</code>
      2. *<code>uaac member add acs.attributes.read app_admin_1</code>
      3. *<code>uaac member add acs.policies.write app_admin_1</code>
      4. *<code>uaac member add acs.attributes.write app_admin_1</code>
15. Setup Manifest 
   Set ClientId, Asset name, Timeseries name, ACS name, UAA name in manifest
      Manifest are created dynamically using the manifest template.The script writes a manifest.yml file using the manifest.yml.template. The script substitutes the ${UAA_SERVICE} and other variables defined for other services with the actual value of the service intances created in the above steps . Below is a sample of the manifest.yml and corresponding template file .

Sample of *manifest.template.yml* 
```applications:
  - name: integration-rmd-datasource
    buildpack: java_buildpack
    path: target/datasource-service-1.1.2-SNAPSHOT.jar
    memory: 2GB
    instance : 2
    services:
        - ${assetService}
        - ${timeSeriesService}
        - ${uaaService}
        - ${acsService} 
``` 
Sample ** template.yml**

``` applications:
  - name: integration-rmd-datasource
    buildpack: java_buildpack
    path: target/datasource-service-1.1.2-SNAPSHOT.jar
    memory: 2GB
    instance : 2
    services:
        - rmd_asset_test
        - rmd_time_series_test
        - rmd_uaa_test
        - rmd_acs_test 
```
  16. Push data-seed, data-ingestion, machine-datasimulator, websocket-server, rmd-datasource, rmd-analytics, fdh-router, rmd-orchestration, rmd-ref-app-ui.
    `cf push rmd_dataseed_${APP_NAME}  -f ${BASEDIR}/dataseed-service/manifest.yml`
17. Run Dataseed to load Spreadsheet data
  The script uploads the AssetData.xls file via the dataingestion rest API call .
      `curl -F \"username=app_user_1}\" -F \"password=app_user_1\" -F \"file=@./data-seed-service/dataseed-service/src/main/resources/rmdapp/AssetData.xls\`
18. Launch Machine Simulator 
      `cf push rmd_machine_simulator_${APP_NAME} -f ./machinedata-simulator/manifest.yml`
19. Deployed UI application 
     1. Create redis `cf cs redis-1 beta rmd_redis_${APP_NAME}` , update the manifest this service instance name.
     2. Run npm  `npm install`
     3. Get bower dependencies `bower install`
     4. Generate a distro for deployment ` grunt dist`
     5. Deploy to Cloud foundry  `cf push rmd_ref_app_ui_${APP_NAME} -f ./rmd-ref-app-ui/mainfest.yml`
20. Stop the Machine simulator
      The machine simulator is running  for couple of minutes , till the script finish deploying the UI application . After the UI application is pushed to cloud foundry . The machine simulator service is shut down.
      `cf stop rmd_machine_simulator_${APP_NAME}`

**Visit your live Reference App in the browser : https://rmd_ref_app_ui_${APP_NAME}.run.aws-usw02-pr.ice.predix.io**

Visit the DataSeedService to *re-load* asset data in to the Predix Reference App : https://data-seed-${APP_NAME}..run.aws-usw02-pr.ice.predix.io

After uploading the asset data, *restart* the machine data simulator with this command to ingest timeseries data `cf start rmd_machine_simulator_${APP_NAME}`



