#!/usr/bin/python
# File: ciscomeraki_search_devices.py

import phantom.app as phantom

from actions import BaseAction
from ciscomeraki_consts import *


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
                params[param] = (
                    [value.strip() for value in self._param[param].split(",") if value.strip()] if param == "tags" else self._param[param]
                )
        self._connector.debug_print("Params --->", params)
        try:
            # Make REST call
            ret_val, response = self._connector._utils._make_rest_call(
                SEARCH_DEVICES.format(organization_id=self._param["organization_id"]),
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

            return self._action_result.set_status(phantom.APP_SUCCESS)

        except Exception as e:
            error_message = self._connector._utils._get_error_message_from_exception(e)
            return self._action_result.set_status(phantom.APP_ERROR, f"Error occurred: {error_message}")
