# File: mxtoolbox_connector.py
#
# Copyright (c) 2016-2022 Splunk Inc.
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
#
#
import ipaddress

import phantom.app as phantom
import requests
import simplejson as json
from phantom.app import ActionResult, BaseConnector

from mxtoolbox_consts import *


class MxtoolboxConnector(BaseConnector):
    # Actions that are supported by this connector
    # Actions are limited to a couple of things on the API due to the very low (64) limit

    def __init__(self):

        # Call the super BaseConnector class init first
        super(MxtoolboxConnector, self).__init__()

    def initialize(self):
        """ Called once for every action.  All initialization things come here.  URL, and whatnot. """

        config = self.get_config()

        self._base_url = MXTOOLBOX_BASE_URL

        self._auth_method = "api key"

        self._key = config.get(MXTOOLBOX_JSON_API_TOKEN)

        # Setting the header to an authorization allows the user to skip logging in and provide the api key only.
        self._headers = {'Authorization': self._key}

        self.set_validator("ipv6", self._is_ip)

        return phantom.APP_SUCCESS

    def _is_ip(self, input_ip_address):
        """ Function that checks given address and return True if address is valid IPv4 or IPV6 address.

        :param input_ip_address: IP address
        :return: status (success/failure)
        """

        ip_address_input = input_ip_address

        try:
            ipaddress.ip_address(str(ip_address_input))
        except:
            return False

        return True

    def _make_rest_call(self, endpoint, action_result, headers={}, params=None, data=None, method="get"):
        """ Makes the actual rest call for any action that requires a rest call.  Returns success or fail, and
            the response """

        # Update the header
        headers.update(self._headers)

        # Init empty resp
        resp_json = None

        request_func = getattr(requests, method)

        # Error checking for valid call method
        if (not request_func):
            action_result.set_status(phantom.APP_ERROR, MXTOOLBOX_ERR_API_UNSUPPORTED_METHOD, method=method)

        # Start actual rest call progress message
        self.save_progress('Using {0} for authentication'.format(self._auth_method))

        try:
            r = request_func(self._base_url + endpoint,
                             headers=headers,
                             verify=False)
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, MXTOOLBOX_ERR_SERVER_CONNECTION, e), resp_json

        # Try to parse the response JSON.  Will except if the response is not a valid json
        try:
            resp_json = r.json()
        except Exception as e:
            msg_string = MXTOOLBOX_ERR_JSON_PARSE.format(url=endpoint, raw_text=r.text)
            return action_result.set_status(phantom.APP_ERROR, msg_string, e), resp_json

        # This if/else block is the final decider for whether the action returns as SUCCESS or failure.
        if (200 <= r.status_code <= 399):
            return phantom.APP_SUCCESS, resp_json
        else:
            details = json.dumps(resp_json).replace('{', '').replace('}', '')
            return action_result.set_status(phantom.APP_ERROR, MXTOOLBOX_ERR_FROM_SERVER.format(status=r.status_code, detail=details)), resp_json

    def _test_connectivity(self, param):
        """ This action tests the connectivity to the Mxtoolbox API.  It must make one call to the API which counts
            against the daily limit.  Test wisely. """

        # Send connectivity progress message
        self.save_progress(MXTOOLBOX_USING_BASE_URL, base_url=MXTOOLBOX_BASE_URL)

        # Send ellipses progress message
        self.save_progress(phantom.APP_PROG_CONNECTING_TO_ELLIPSES, MXTOOLBOX_BASE_URL)

        # Declare the endpoint
        endpoint = MXTOOLBOX_TEST_CONNECTION_ENDPOINT

        # Create an action result to be passed to the rest call function
        action_result = ActionResult()

        # Start progress message of rest call
        self.save_progress(MXTOOLBOX_MSG_GET_INCIDENT_TEST)

        # Call the rest call function
        ret_val, response = self._make_rest_call(endpoint, action_result, params=param)

        if (phantom.is_fail(ret_val)):
            self.debug_print(action_result.get_message())

            self.set_status(phantom.APP_ERROR, action_result.get_message())

            self.append_to_message(MXTOOLBOX_ERR_CONNECTIVITY_TEST)

            return phantom.APP_ERROR
        self.save_progress(MXTOOLBOX_SUCC_CONNECTIVITY_MESSAGE)
        return self.set_status_save_progress(phantom.APP_SUCCESS, MXTOOLBOX_SUCC_CONNECTIVITY_TEST)

    def _lookup_domain(self, param):

        action_result = self.add_action_result(ActionResult(dict(param)))

        self.save_progress(MXTOOLBOX_USING_BASE_URL, base_url=self._base_url)

        self.save_progress(phantom.APP_PROG_CONNECTING_TO_ELLIPSES, MXTOOLBOX_BASE_URL)

        command = param.get(MXTOOLBOX_JSON_COMMAND, False)

        if isinstance(command, bool):

            ip = param[MXTOOLBOX_JSON_IP]
            ip = ipaddress.ip_address(ip).exploded
            domain = MXTOOLBOX_DOMAIN_LINK.format(domain=ip)

            endpoint = MXTOOLBOX_BASE_ENDPOINT_URL.format(type="ptr", domain=domain)

        else:

            domain = param[MXTOOLBOX_JSON_DOMAIN]

            endpoint = MXTOOLBOX_BASE_ENDPOINT_URL.format(type=command, domain=domain)

        ret_val, response = self._make_rest_call(endpoint, action_result)

        # Handle failures (if any)
        if (phantom.is_fail(ret_val)):
            self.debug_print(action_result.get_message())
            self.set_status(phantom.APP_ERROR, action_result.get_message())
            return phantom.APP_ERROR

        needed = ["Status", "IP Address", "TTL", "Domain Name"]

        if isinstance(command, bool):
            needed.append("PTR")
        elif command == "spf":
            needed.extend(["Prefix", "Type", "Value", "PrefixDesc", "Description"])
        elif command == "txt":
            needed.extend(["Type", "Record"])
        elif command == "soa":
            needed.extend(["Type", "Primary NS", "Responsible Email"])

        # Get the usable, important information from "Information"
        for elem in response[MXTOOLBOX_JSON_RESP_KEY]:
            temp_dict = {}

            for key, value in elem.items():
                if key in needed:
                    temp_dict[key.replace(" ", "_")] = value

            if temp_dict:
                action_result.add_data(temp_dict)

        if (len(response[MXTOOLBOX_JSON_RESP_KEY]) < 1):
            return (action_result.set_status(phantom.APP_ERROR, MXTOOLBOX_ERROR_LOOKUP_NO_DATA_FOUND))

        action_result.set_summary({"total_objects": len(response[MXTOOLBOX_JSON_RESP_KEY])})

        return action_result.set_status(phantom.APP_SUCCESS)

    def handle_action(self, param):
        """ All actions go through here first to be piped to the correct place. """

        action = self.get_action_identifier()

        ret_val = phantom.APP_SUCCESS

        if (action == phantom.ACTION_ID_TEST_ASSET_CONNECTIVITY):
            ret_val = self._test_connectivity(param)
        elif (action == ACTION_ID_LOOKUP_DOMAIN):
            ret_val = self._lookup_domain(param)
        elif (action == ACTION_ID_LOOKUP_IP):
            ret_val = self._lookup_domain(param)
        return ret_val


if __name__ == '__main__':
    """ This section is executed when run in standalone debug mode """

    import sys

    import pudb

    pudb.set_trace()

    with open(sys.argv[1]) as f:
        in_json = f.read()
        in_json = json.loads(in_json)
        print(json.dumps(in_json, indent=' ' * 4))

        connector = MxtoolboxConnector()

        connector.print_progress_message = True

        ret_val = connector._handle_action(json.dumps(in_json), None)

        print(ret_val)

    exit(0)
