##Asset Model
Since Predix Asset comes with an empty database, the Reference App creates a data 'model' depicted below, which sets up entities and attributes for Groups, Classifications, Assets and Meters.

Note: Meter will change to Parameter in a future release

<img src=/images/AssetModel.png width=1500 height=600>

The model has these characteristics:
- A Turbine, for example,  is Modeled as a Classification
- (future)A Device, such as a Honeywell Controller, is modeled as a Classification
- (future)A DeviceMeter is hooked to Predix Machine and a data Node retrieves data using an Adapter.  
- An AssetMeter is hooked to Predix Machine and a data Node retrieves data using an Adapter.  
- A Predix Machine can talk to many Devices on many Industrial Machines
- A Meter represents a Timeseries Data parameter, either raw sensor data or calculated data
- (future)A DeviceAsset is an instance of a Device classification and has DeviceMeter instance attributes
- An AssetGroup can be a location (Site,Plant,etc) or an entity(Enterprise,City,County) that logically holds a set of Assets
- An Asset is an instance of a Classification and has singleValue Attributes as well as AssetMeter instance attributes
- AssetMeter knows of it's Unit of Measure and also has a key to several Datasources
DeviceMeter ID
Node ID
Timeseries Tag ID
- A Field further describes any Attribute for purposes such as DataIngestion, UI, DataBinding for FederatedQuery, Analytics
- A Field has a FieldSource that describes how or where the data is stored for an Attribute
- A Field has a DataHandler uri that knows how to retrieve or store data from/to a FieldSource
- (future)A MachineAsset can be modeled to navigate from the Machine Id to the Devices and Assets
