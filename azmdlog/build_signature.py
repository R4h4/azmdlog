import base64
import hmac
import hashlib


class AzureMonitorSignature:
    """
    Signature builder for Azure Monitor.
    """

    def __init__(self, workspace_id : str, shared_key: str):
        """
        :param workspace_id : Azure Monitor customer id
        :param shared_key: Azure Monitor shared key
        """
        self.workspace_id = workspace_id
        self.shared_key = shared_key

    def build_signature(self, date: str, content_length: int, method: str, content_type: str, resource: str) -> str:
        """
        Build the signature for the Azure Monitor API request.

        :param date: Date in RFC1123 format
        :param content_length: Content length of the request body
        :param method: HTTP request method
        :param content_type: Content type of the request body
        :param resource: API resource
        :return: The Azure Monitor authorization signature
        """
        x_headers = 'x-ms-date:' + date
        string_to_hash = method + "\n" + str(content_length) + "\n" + content_type + "\n" + x_headers + "\n" + resource
        bytes_to_hash = str.encode(string_to_hash, 'utf-8')
        decoded_key = base64.b64decode(self.shared_key)
        encoded_hash = (
            base64.b64encode(hmac.new(decoded_key, bytes_to_hash, digestmod=hashlib.sha256).digest())).decode()
        authorization = "SharedKey {}:{}".format(self.workspace_id, encoded_hash)
        return authorization
