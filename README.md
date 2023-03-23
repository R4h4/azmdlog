# Azure Monitor Custom Logger for Databricks

This project provides a custom logger for Azure Databricks to log information in a structured JSON format to Azure Monitor. The logger is built as a custom handler for the standard Python logging module, making it easy to integrate into your Databricks notebooks and applications.

## Requirements

- Python 3.6+
- Requests library

## Installation

You can install this libraries using pip:

```sh
pip install azmdlog
```

## Usage
This library is meant to be used inside of an Azure Databricks Notebook.

To use the custom logger, import the AzureMonitorHandler and AzureMonitorFormatter classes from the azmdlog.azure_monitor_handler module, and configure them with your Azure Monitor Workspace's customer ID and shared key.

Here's an example of how to configure the logger:

```python
import logging
from azmdlog import AzureMonitorHandler, AzureMonitorFormatter

customer_id = "your_customer_id"
shared_key = "your_shared_key"

def get_dbutils(spark: SparkSession):
    if spark.conf.get("spark.databricks.service.client.enabled") == "true":
        from pyspark.dbutils import DBUtils
        return DBUtils(spark)
    else:
        import IPython
        return IPython.get_ipython().user_ns["dbutils"]

dbutils = get_dbutils(spark)

# Configure the logger
logger = logging.getLogger("databricks_custom_logger")
logger.setLevel(logging.INFO)

# Create and configure the Azure Monitor handler
handler = AzureMonitorHandler(customer_id, shared_key)
handler.setLevel(logging.INFO)
handler.setFormatter(AzureMonitorFormatter(dbutils))

# Add the handler to the logger
logger.addHandler(handler)

# Log messages
logger.info("This is an informational message.")
logger.error("This is an error message.")
```
Replace "your_customer_id" and "your_shared_key" with your Azure Monitor Workspace's customer ID and shared key, respectively.

The logger will send log messages as JSON objects to Azure Monitor, including the following additional fields:

- Application: The notebook path
- ClusterId: The cluster ID
- SessionId: The session ID
- Who: The user

These fields are automatically populated using the dbutils object.

## Testing
To run the tests, you will need the pytest library. Install it using pip:

```sh
pip install pytest
```
Navigate to your project's root directory and run pytest:

```sh
pytest
```
This will run the unit tests and display the results.