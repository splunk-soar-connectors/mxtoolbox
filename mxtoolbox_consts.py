# File: mxtoolbox_consts.py
#
# Copyright (c) 2016-2025 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.
MXTOOLBOX_BASE_URL = "https://mxtoolbox.com/api/v1/"
MXTOOLBOX_BASE_ENDPOINT_URL = "lookup/{type}/{domain}"
MXTOOLBOX_DOMAIN_LINK = "?argument={domain}"

MXTOOLBOX_ERR_API_UNSUPPORTED_METHOD = "Unsupported method"
MXTOOLBOX_ERR_CONNECTIVITY_TEST = "Test Connectivity Failed"
MXTOOLBOX_ERR_FROM_SERVER = "API failed, Status code: {status}, Detail: {detail}"
MXTOOLBOX_ERR_JSON_PARSE = "Unable to parse reply as a Json from URL {url}. raw string reply: '{raw_text}'"
MXTOOLBOX_ERR_SERVER_CONNECTION = "Connection failed"
MXTOOLBOX_ERR_INVALID_TYPE = "Invalid type for lookup."
MXTOOLBOX_JSON_RESP_KEY = "Information"
MXTOOLBOX_JSON_API_TOKEN = "api_token"
MXTOOLBOX_JSON_COMMAND = "type"
MXTOOLBOX_JSON_DOMAIN = "domain"
MXTOOLBOX_JSON_IP = "ip"
MXTOOLBOX_JSON_PER_PAGE = "max_results_per_page"
MXTOOLBOX_JSON_PAGE = "page_number"
MXTOOLBOX_JSON_PORT = "port"

MXTOOLBOX_MESSAGE_GET_INCIDENT_TEST = "Querying google.com. . ."

MXTOOLBOX_SUCC_LOOKUP = "Successfully received {type} of {domain}."
MXTOOLBOX_SUCC_CONNECTIVITY_MESSAGE = "Successfully queried google.com and received a JSON reply."
MXTOOLBOX_SUCC_CONNECTIVITY_TEST = "Test Connectivity Passed"

MXTOOLBOX_TEST_CONNECTION_ENDPOINT = "lookup/dns/google.com"
MXTOOLBOX_TEST_FAILURE = "Invalid API key."

MXTOOLBOX_USING_BASE_URL = "Using url: {base_url}"
MXTOOLBOX_USING_PORT = "?port={port}"

ACTION_ID_LOOKUP_DOMAIN = "lookup_domain"
ACTION_ID_LOOKUP_IP = "lookup_ip"
MXTOOLBOX_ERR_LOOKUP_NO_DATA_FOUND = "Lookup did not return any useful information."
