from __future__ import absolute_import
import logging
from unittest.mock import MagicMock, patch, ANY

import pytest
from pyspark.sql import SparkSession

from azmdlog import AzureMonitorHandler, AzureMonitorFormatter
from azmdlog.build_signature import AzureMonitorSignature


@pytest.fixture
def spark_session():
    return MagicMock(spec=SparkSession)


@pytest.fixture
def dbutils_mock():
    dbutils = MagicMock()
    dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get.return_value = "Application"
    dbutils.notebook.entry_point.getDbutils().notebook().getContext().tags().apply.side_effect = lambda key: key
    return dbutils


def test_azure_monitor_handler_emit(dbutils_mock):
    with patch("azmdlog.azure_monitor_handler.AzureMonitorHandler.post_data") as post_data_mock:
        handler = AzureMonitorHandler("workspace_id", "shared_key", dbutils_mock)
        handler.setFormatter(AzureMonitorFormatter(dbutils_mock))
        logger = logging.getLogger("test_logger")
        logger.addHandler(handler)

        logger.error("test message", {'eventName': 'bigFailure'})

        post_data_mock.assert_called_once()
        assert "test message" in post_data_mock.call_args[0][0]


def test_azure_monitor_formatter(dbutils_mock):
    formatter = AzureMonitorFormatter(dbutils_mock)
    record = logging.LogRecord("test_logger", logging.ERROR, "test", 1, "test message", [{'eventName': 'testEvent'}], None)

    formatted_log = formatter.format(record)
    assert formatted_log.startswith('[{"TimeStamp": "')
    assert '"Level": "ERROR"' in formatted_log
    assert '"Message": "test message"' in formatted_log
    assert '"eventName": "testEvent"' in formatted_log
    assert '"Application": "Application"' in formatted_log
    assert '"ClusterId": "clusterId"' in formatted_log
    assert '"SessionId": "sessionId"' in formatted_log
    assert '"User": "user"' in formatted_log


def test_azure_monitor_signature():
    signature_builder = AzureMonitorSignature("workspace_id", "shared_key1==")

    with patch("base64.b64encode") as b64encode_mock, patch("hmac.new") as hmac_mock:
        b64encode_mock.return_value = b"encoded_hash"
        hmac_mock.return_value = MagicMock()
        hmac_mock.return_value.digest.return_value = b"digest"

        result = signature_builder.build_signature("date", 10, "method", "content_type", "resource")

        assert result == "SharedKey workspace_id:encoded_hash"


def test_azure_monitor_handler_post_data():
    handler = AzureMonitorHandler("workspace_id", "shared_key1==")

    # Mock the AzureMonitorSignature.build_signature method
    with patch("azmdlog.azure_monitor_handler.AzureMonitorSignature.build_signature") as build_signature_mock:
        build_signature_mock.return_value = "mocked_signature"

        # Mock the requests.post method
        with patch("requests.post") as post_mock:
            post_mock.return_value.status_code = 200

            body = '[{"key": "value"}]'
            result = handler.post_data(body)

            # Assert that the result is 'Accepted'
            assert result == "Accepted"

            # Assert that the POST request was called with the correct headers and data
            post_mock.assert_called_once_with(
                "https://workspace_id.ods.opinsights.azure.com/api/logs?api-version=2016-04-01",
                data=body,
                headers={
                    "content-type": "application/json",
                    "Authorization": "mocked_signature",
                    "Log-Type": "DatabricksCustomLogs",
                    "x-ms-date": ANY
                },
            )
