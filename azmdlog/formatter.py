import logging
import json


class AzureMonitorFormatter(logging.Formatter):
    """
    A custom formatter for Azure Monitor.
    """

    def __init__(self, dbutils):
        """
        Initialize the AzureMonitorFormatter.

        :param dbutils: Databricks utility object
        """
        super().__init__(fmt="%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        self.event_name = ''
        self.dbutils = dbutils

    def format(self, record: logging.LogRecord) -> str:
        """
        Format a log entry for Azure Monitor.

        :param record: Log record to format
        :return: Formatted log entry as a JSON string
        """
        formatted_message = super().format(record)
        log_data = {
            "TimeStamp": record.asctime,
            "Level": record.levelname,
            "Message": record.message,
            "Application": self.dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get(),
            "ClusterId": self.dbutils.notebook.entry_point.getDbutils().notebook().getContext().tags().apply('clusterId'),
            "SessionId": self.dbutils.notebook.entry_point.getDbutils().notebook().getContext().tags().apply('sessionId'),
            "User": self.dbutils.notebook.entry_point.getDbutils().notebook().getContext().tags().apply('user'),
            "formatted_message": formatted_message
        }
        if record.args:
            log_data.update(record.args)
        return json.dumps([log_data])
