#!/usr/bin/python
# File: ciscomeraki_search_organization_clients.py
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


class SearchOrganizationClients(BaseAction):
    """Class to handle the search organization clients action."""

    def execute(self):
        """Execute the search organization clients action.

        Returns:
            bool: Success/failure
        """
        self._connector.save_progress(consts.EXECUTION_START_MSG.format("search_organization_clients"))

        # Validate required parameters
        organization_id = self._param.get("organization_id")
        if not organization_id:
            return self._action_result.set_status(phantom.APP_ERROR, consts.ERROR_REQUIRED_PARAM.format(key="organization_id"))

        mac = self._param.get("mac")
        if not mac:
            return self._action_result.set_status(phantom.APP_ERROR, consts.ERROR_REQUIRED_PARAM.format(key="mac"))

        # Validate per_page if provided
        per_page = self._param.get("per_page")
        if per_page:
            try:
                per_page = int(per_page)
                if not 3 <= per_page <= 5:
                    return self._action_result.set_status(phantom.APP_ERROR, "Parameter 'per_page' must be between 3 and 5")
            except ValueError:
                return self._action_result.set_status(phantom.APP_ERROR, consts.ERROR_INVALID_INT_PARAM.format(key="per_page"))

        # Prepare parameters
        params = {"mac": mac}
        if per_page:
            params["perPage"] = per_page

        # Make REST call
        ret_val, response = self._connector._utils._make_rest_call(
            endpoint=consts.SEARCH_ORGANIZATION_CLIENTS.format(organization_id=organization_id),
            action_result=self._action_result,
            method="get",
            params=params,
        )

        if phantom.is_fail(ret_val):
            return self._action_result.get_status()

        # Process response - API returns a single client object with records
        self._action_result.add_data(response)

        # Build summary
        summary = {
            "client_id": response.get("clientId", ""),
            "mac": response.get("mac", ""),
            "total_records": len(response.get("records", [])),
        }
        self._action_result.update_summary(summary)

        return self._action_result.set_status(
            phantom.APP_SUCCESS,
            consts.ACTION_SUCCESS_RESPONSE.format(
                action=" ".join([i.capitalize() if idx > 0 else i for idx, i in enumerate(self._connector.get_action_identifier().split("_"))])
            ),
        )
