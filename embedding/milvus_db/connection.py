from pymilvus import connections, utility

class MilvusConnection:
    def __init__(self, alias="default", host="localhost", port="19530"):
        self.alias = alias
        self.host = host
        self.port = port
        self.connected = False

    def connect(self):
        if not self.connected or not utility.has_connection(self.alias):
            try:
                print(f"Connecting to Milvus at {self.host}:{self.port}...")
                connections.connect(self.alias, host=self.host, port=self.port)
                self.connected = True
                print("Successfully connected to Milvus.")
            except Exception as e:
                print(f"Failed to connect to Milvus: {e}")
                raise
        else:
            print("Already connected to Milvus.")

    def disconnect(self):
        if self.connected:
            connections.disconnect(self.alias)
            self.connected = False
            print("Disconnected from Milvus.")

milvus_connection = MilvusConnection()