#!/usr/bin/python
# File: ciscomeraki_list_org_license_states.py
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


class ListOrgLicenseStates(BaseAction):
    """Class to handle the list organization license states action."""

    def _validate_params(self):
        """Validate parameters.

        Returns:
            bool: Success/failure
        """
        organization_id = self._param.get("organization_id")
        if not organization_id:
            return self._action_result.set_status(phantom.APP_ERROR, ERROR_REQUIRED_PARAM.format(key="organization_id"))

        return phantom.APP_SUCCESS

    def execute(self):
        """Execute the list organization license states action.

        Returns:
            bool: Success/failure
        """
        # self._param = self._connector.get_current_param()
        # self._action_result = self._connector.add_action_result(ActionResult(dict(self._param)))

        # Validate parameters
        if phantom.is_fail(self._validate_params()):
            return self._action_result.get_status()

        organization_id = self._param["organization_id"]

        try:
            # Make REST call
            ret_val, response = self._connector._utils._make_rest_call(
                ORG_LICENSE_STATE.format(organization_id=organization_id), self._action_result, "get"
            )

            if phantom.is_fail(ret_val):
                self._connector.debug_print("Failing --->", ret_val)
                self._connector.debug_print("message  --->", self._action_result.get_status())
                return self._action_result.get_status()

            # Add the license state data
            self._action_result.add_data(response)

            # Add summary
            summary = {
                "license_status": response.get("status", "unknown"),
                "total_licenses": len(response.get("licenses", [])),
                "expiration_date": response.get("expirationDate"),
            }
            self._action_result.update_summary(summary)

            return self._action_result.set_status(phantom.APP_SUCCESS)

        except Exception as e:
            error_message = self._connector._utils._get_error_message_from_exception(e)
            return self._action_result.set_status(phantom.APP_ERROR, f"Error occurred: {error_message}")
