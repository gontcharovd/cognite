from airflow.hooks.base_hook import BaseHook
from cognite.client import CogniteClient


class CogniteHook(BaseHook):
    """Hook for the Cognite API.

    Abstracts details of the Cognite API and provides several convenience
    methods for fetching data (e.g. get timeseries, sensors, data) from the API.
    Also provides support for authentication, etc.

    Args:
        api_key (str): the Cognite API key
        client_name (str): name of the cognite client
        project (str): the name of the Open Industrial Data Project
    """

    DEFAULT_CLIENT_NAME = 'cognite'
    DEFAULT_PROJECT = 'publicdata'

    def __init__(self, api_key, client_name, project):
        super().__init__(source=None)
        self.api_key = api_key
        self.client_name = client_name
        self.project = clientproject

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """Closes any active session. """
        if self.session:
            self.session.close()
        self.client = None

    def get_client(self):
        if not self.api_key:
            raise ValueError('No api_key specified.')

        self.client = CogniteClient(
            api_key=self.api_key,
            client_name=self.client_name or DEFAULT_CLIENT_NAME,
            project=self.project or DEFAULT_PROJECT
        )
        return self.client
