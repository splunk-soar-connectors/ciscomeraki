#!/usr/bin/python
# File: ciscomeraki_list_l3_firewall_rules.py
#
# Copyright (c) 2025 Splunk Inc.
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

import phantom.app as phantom

from actions import BaseAction
from ciscomeraki_consts import *


class ListL3FirewallRules(BaseAction):
    """Class to handle the list L3 firewall rules action."""

    def _validate_params(self):
        network_id = self._param.get("network_id")
        if not network_id:
            return self._action_result.set_status(phantom.APP_ERROR, ERROR_REQUIRED_PARAM.format(key="network_id"))
        return phantom.APP_SUCCESS

    def execute(self):
        """Execute the list L3 firewall rules action.

        Returns:
            bool: Success/failure
        """
        self._connector.save_progress(EXECUTION_START_MSG.format("list_l3_firewall_rules"))

        # self._param = self._connector.get_current_param()
        #       self._action_result = self._connector.add_action_result(ActionResult(dict(self._param)))

        # Validate parameters
        if phantom.is_fail(self._validate_params()):
            return self._action_result.get_status()

        # Prepare parameters
        params = {}
        network_id = self._param["network_id"]

        # Make REST call
        ret_val, response = self._connector._utils._make_rest_call(
            endpoint=LIST_L3_FIREWALL_RULES.format(network_id=network_id), action_result=self._action_result, method="get"
        )

        if phantom.is_fail(ret_val):
            return self._action_result.get_status()

        # Process response
        try:
            self._connector.debug_print("response in process--->", response)
            for rule in response.get("rules", []):
                self._action_result.add_data(rule)
            summary = {"total_rules": len(response)}
            self._action_result.update_summary(summary)
            return self._action_result.set_status(
                phantom.APP_SUCCESS, ACTION_SUCCESS_RESPONSE.format(action=self._connector.get_action_identifier())
            )
        except Exception as e:
            error_message = self._connector._utils._get_error_message_from_exception(e)
            return self._action_result.set_status(phantom.APP_ERROR, f"Error processing response: {error_message}")
