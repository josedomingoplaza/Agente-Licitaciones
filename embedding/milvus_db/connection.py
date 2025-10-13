from pymilvus import connections, utility
import os
import time


class MilvusConnection:
    def __init__(self, alias="default", host=None, port=None):
        # read defaults from environment (compose .env will populate these)
        self.alias = alias
        self.host = host or os.environ.get("MILVUS_HOST", "milvus")
        self.port = port or os.environ.get("MILVUS_PORT", "19530")
        self.connected = False

    def connect(self, retries: int = 3, retry_delay: float = 1.0):
        """Connect to Milvus. Uses environment defaults so it's safe in Docker.

        Will retry a few times on transient failure. This method is idempotent.
        """
        if self.connected and utility.has_connection(self.alias):
            return

        last_exc = None
        for attempt in range(1, retries + 1):
            try:
                print(f"Connecting to Milvus at {self.host}:{self.port} (attempt {attempt})...")
                connections.connect(self.alias, host=self.host, port=self.port)
                self.connected = True
                print("Successfully connected to Milvus.")
                return
            except Exception as e:
                print(f"Connection attempt {attempt} failed: {e}")
                last_exc = e
                time.sleep(retry_delay)

        # re-raise last exception after retries
        raise last_exc

    def disconnect(self):
        if self.connected:
            try:
                connections.disconnect(self.alias)
            finally:
                self.connected = False


# Export a connection manager instance; it reads MILVUS_HOST/MILVUS_PORT from env
milvus_connection = MilvusConnection()