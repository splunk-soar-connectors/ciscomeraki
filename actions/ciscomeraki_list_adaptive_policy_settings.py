#!/usr/bin/python
# File: ciscomeraki_list_adaptive_policy_settings.py
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

import ciscomeraki_consts as consts
from actions import BaseAction


class ListAdaptivePolicySettings(BaseAction):
    """Class to handle the list adaptive policy settings action."""

    def _validate_params(self):
        organization_id = self._param.get("organization_id")
        if not organization_id:
            return self._action_result.set_status(phantom.APP_ERROR, consts.ERROR_REQUIRED_PARAM.format(key="organization_id"))
        return phantom.APP_SUCCESS

    def execute(self):
        # self._param = self._connector.get_current_param()
        # self._action_result = self._connector.add_action_result(ActionResult(dict(self._param)))

        # Validate parameters
        if phantom.is_fail(self._validate_params()):
            return self._action_result.get_status()

        organization_id = self._param["organization_id"]

        # Make REST call
        ret_val, response = self._connector._utils._make_rest_call(
            consts.LIST_ADAPTIVE_POLICY_SETTINGS.format(organization_id=organization_id),
            self._action_result,
            "get",
        )

        if phantom.is_fail(ret_val):
            return self._action_result.get_status()

        # Process response
        try:
            for setting in response:
                self._action_result.add_data(setting)
            summary = {"total_settings": len(response)}
            self._action_result.update_summary(summary)
            return self._action_result.set_status(phantom.APP_SUCCESS)
        except Exception as e:
            error_message = self._connector._utils._get_error_message_from_exception(e)
            return self._action_result.set_status(phantom.APP_ERROR, f"Error processing response: {error_message}")
