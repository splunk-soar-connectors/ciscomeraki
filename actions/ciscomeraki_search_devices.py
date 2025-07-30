# Copyright (c) 2025 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#!/usr/bin/python
# File: ciscomeraki_search_devices.py

import phantom.app as phantom

import ciscomeraki_consts as consts
from actions import BaseAction


class SearchDevices(BaseAction):
    """Class to handle the search devices action."""

    def _validate_params(self):
        """Validate parameters.

        Returns:
            bool: Success/failure
        """
        # At least one search parameter should be provided
        search_params = ["organization_id", "mac", "serial", "model", "tags"]
        if not any(self._param.get(param) for param in search_params):
            return self._action_result.set_status(
                phantom.APP_ERROR, "At least one search parameter (organization_id, mac, serial, model, or tags) must be provided"
            )

        return phantom.APP_SUCCESS

    def execute(self):
        """Execute the search devices action.

        Returns:
            bool: Success/failure
        """

        # Validate parameters
        if phantom.is_fail(self._validate_params()):
            return self._action_result.get_status()

        # Build search parameters
        params = {}
        for param in ["organization_id", "mac", "serial", "model", "tags"]:
            if self._param.get(param):
                if param == "tags":
                    tag_list = [value.strip() for value in self._param[param].split(",") if value.strip()]
                    if tag_list:  # Only add if there are actual tags
                        params["tags[]"] = tag_list
                else:
                    params[param] = self._param[param]
        try:
            # Make REST call
            ret_val, response = self._connector._utils._make_rest_call(
                consts.SEARCH_DEVICES.format(organization_id=self._param["organization_id"]),
                method="get",
                action_result=self._action_result,
                params=params,
            )

            if phantom.is_fail(ret_val):
                return self._action_result.get_status()

            # Process each device in the response
            for device in response:
                self._action_result.add_data(device)

            # Add summary
            summary = {"total_devices_found": len(response), "search_criteria": ", ".join(f"{k}: {v}" for k, v in params.items())}
            self._action_result.update_summary(summary)

            return self._action_result.set_status(
                phantom.APP_SUCCESS,
                consts.ACTION_SUCCESS_RESPONSE.format(
                    action=" ".join(
                        [i.capitalize() if idx > 0 else i for idx, i in enumerate(self._connector.get_action_identifier().split("_"))]
                    )
                ),
            )

        except Exception as e:
            error_message = self._connector._utils._get_error_message_from_exception(e)
            return self._action_result.set_status(phantom.APP_ERROR, f"Error occurred: {error_message}")
