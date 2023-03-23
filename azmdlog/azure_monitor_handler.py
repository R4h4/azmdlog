import logging
import datetime
from typing import Any, Dict

import requests

from .build_signature import AzureMonitorSignature


class AzureMonitorHandler(logging.Handler):
    """
    A custom logging handler for Azure Monitor.
    """

    def __init__(self, workspace_id: str, shared_key: str, log_type: str = "DatabricksCustomLogs"):
        """
        :param workspace_id : Azure Monitor customer id
        :param shared_key: Azure Monitor shared key
        :param log_type: Log type for Azure Monitor
        """
        super().__init__()
        self.workspace_id = workspace_id
        self.shared_key = shared_key
        self.log_type = log_type
        self.signature_builder = AzureMonitorSignature(workspace_id, shared_key)

    def emit(self, record: logging.LogRecord) -> None:
        """
        Emit a log entry.

        :param record: Log record to emit
        """
        log_entry = self.format(record)
        self.post_data(log_entry)

    def post_data(self, body: str) -> str:
        """
        Post data to Azure Monitor.

        :param body: Log entry to post
        :return: Status string, either 'Accepted' or 'Not Accepted'
        """
        method = 'POST'
        content_type = 'application/json'
        resource = '/api/logs'
        rfc1123date = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        content_length = len(body)
        signature = self.signature_builder.build_signature(rfc1123date, content_length, method, content_type, resource)
        uri = f'https://{self.workspace_id}.ods.opinsights.azure.com{resource}?api-version=2016-04-01'

        headers: Dict[str, Any] = {
            'content-type': content_type,
            'Authorization': signature,
            'Log-Type': self.log_type,
            'x-ms-date': rfc1123date
        }
        response = requests.post(uri, data=body, headers=headers)
        if response.ok:
            return 'Accepted'
        else:
            print(f"Response code: {response.status_code}")
            print(f"Response: {response.content}")
            return 'Not Accepted'
