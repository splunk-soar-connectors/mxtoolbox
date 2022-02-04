[comment]: # "Auto-generated SOAR connector documentation"
# MxToolbox

Publisher: Splunk  
Connector Version: 2\.0\.7  
Product Vendor: MxToolbox  
Product Name: MxToolbox  
Product Version Supported (regex): "\.\*"  
Minimum Product Version: 5\.1\.0  

This app implements investigative actions on domains and IPs

### Configuration Variables
The below configuration variables are required for this Connector to operate.  These variables are specified when configuring a MxToolbox asset in SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**api\_token** |  required  | password | API token

### Supported Actions  
[test connectivity](#action-test-connectivity) - Validates the asset configuration for connectivity  
[lookup domain](#action-lookup-domain) - Returns the result of a lookup on a specific url  
[lookup ip](#action-lookup-ip) - Returns the result of a lookup on a specific ip address  

## action: 'test connectivity'
Validates the asset configuration for connectivity

Type: **test**  
Read only: **True**

This action sends a single request to the MxToolbox API\.

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output  

## action: 'lookup domain'
Returns the result of a lookup on a specific url

Type: **investigate**  
Read only: **True**

Lookup types in mission control are limited to\:<ul><li><b>mx</b></li><li><b>a</b></li><li><b>dns</b></li><li><b>spf</b></li><li><b>txt</b></li><li><b>soa</b></li></ul>There is support from MxToolbox for other types of lookups which can be specified within a playbook\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**domain** |  required  | Domain to query | string |  `domain` 
**type** |  required  | Type of domain lookup | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.data\.\*\.TTL | string | 
action\_result\.data\.\*\.Status | string | 
action\_result\.data\.\*\.IP\_Address | string |  `ip` 
action\_result\.data\.\*\.Domain\_Name | string |  `domain` 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary\.total\_objects | numeric | 
action\_result\.parameter\.type | string | 
action\_result\.parameter\.domain | string |  `domain` 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'lookup ip'
Returns the result of a lookup on a specific ip address

Type: **investigate**  
Read only: **True**

This action only uses the lookup type of 'ptr'\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**ip** |  required  | IP to query | string |  `ip`  `ipv6` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.data\.\*\.TTL | string | 
action\_result\.data\.\*\.IP\_Address | string |  `ip`  `ipv6` 
action\_result\.data\.\*\.Domain\_Name | string |  `domain` 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary\.total\_objects | numeric | 
action\_result\.parameter\.ip | string |  `ip`  `ipv6` 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 