**Purpose:**
- Company has multiple orgs of Datadog and needs to pull Billage metrics for hosts and containers into their "main" org.
  
  
*Both files should be in the same directory*

**Files:**
- **hostInfo.txt** - comma seperated file with the format of [name],[apikey],[appkey]
    in the list of orgs, the top one in this file will be the "main org"
    
 - **hosts.py** - script to execute api

**Script Breakdown**
- **Class(es)**
      Org: conatins metadata of org

 - **methods/functions**
    - **getHostData(apikey,appkey)**
        - purpose: pull host and container billable usage for host
        - returns: json of data
        - Note: as of the creation of this script (July 2018), "This is not yet supported by the Python Client for Datadog API"code was written from scratch to accomplish this call. Potentially could need to be updated or in time could have the API available in Python

    - **storeHostDataInOrg(Org Object, Data array)**
        - purpose: save data into Org Object
        
    - **sendMetricToDD(Main Org Name, apikey, appkey, metric name, value)**
        - purpose: send custom metric to DD into "main org"
        
**Flow**
![IMAGE](https://raw.githubusercontent.com/sellarit9/datadog/master/HostScriptFlow.png)

