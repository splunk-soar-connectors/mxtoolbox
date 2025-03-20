# MxToolbox

Publisher: Splunk \
Connector Version: 2.0.8 \
Product Vendor: MxToolbox \
Product Name: MxToolbox \
Minimum Product Version: 5.1.0

This app implements investigative actions on domains and IPs

### Configuration variables

This table lists the configuration variables required to operate MxToolbox. These variables are specified when configuring a MxToolbox asset in Splunk SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**api_token** | required | password | API token |

### Supported Actions

[test connectivity](#action-test-connectivity) - Validates the asset configuration for connectivity \
[lookup domain](#action-lookup-domain) - Returns the result of a lookup on a specific url \
[lookup ip](#action-lookup-ip) - Returns the result of a lookup on a specific ip address

## action: 'test connectivity'

Validates the asset configuration for connectivity

Type: **test** \
Read only: **True**

This action sends a single request to the MxToolbox API.

#### Action Parameters

No parameters are required for this action

#### Action Output

No Output

## action: 'lookup domain'

Returns the result of a lookup on a specific url

Type: **investigate** \
Read only: **True**

Lookup types in mission control are limited to:<ul><li><b>mx</b></li><li><b>a</b></li><li><b>dns</b></li><li><b>spf</b></li><li><b>txt</b></li><li><b>soa</b></li></ul>There is support from MxToolbox for other types of lookups which can be specified within a playbook.

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**domain** | required | Domain to query | string | `domain` |
**type** | required | Type of domain lookup | string | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.data.\*.TTL | string | | 24 hrs |
action_result.data.\*.Status | string | | [Green] |
action_result.data.\*.IP_Address | string | `ip` | 10.1.1.99 |
action_result.data.\*.Domain_Name | string | `domain` | a.iana-server.net |
action_result.status | string | | success failed |
action_result.message | string | | Total Objects: 4 |
action_result.summary.total_objects | numeric | | 4 |
action_result.parameter.type | string | | dns |
action_result.parameter.domain | string | `domain` | example.com |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'lookup ip'

Returns the result of a lookup on a specific ip address

Type: **investigate** \
Read only: **True**

This action only uses the lookup type of 'ptr'.

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**ip** | required | IP to query | string | `ip` `ipv6` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.data.\*.TTL | string | | 24 hrs |
action_result.data.\*.IP_Address | string | `ip` `ipv6` | 10.1.1.9 |
action_result.data.\*.Domain_Name | string | `domain` | example.com |
action_result.status | string | | success failed |
action_result.message | string | | Total Objects: 4 |
action_result.summary.total_objects | numeric | | 4 |
action_result.parameter.ip | string | `ip` `ipv6` | 10.1.1.9 |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

______________________________________________________________________

Auto-generated Splunk SOAR Connector documentation.

Copyright 2025 Splunk Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
