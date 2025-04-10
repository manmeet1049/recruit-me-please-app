from marqo import Client
from marqo.errors import MarqoWebError


class MarqoIndexer:
    def __init__(
        self,
        url: str,
        index_name: str,
        model: str = "hf/all-MiniLM-L6-v2",
        tensor_fields=None,
    ):
        self.client = Client(url)
        self.index_name = index_name
        self.model = model
        self.tensor_fields = tensor_fields or ["text"]
        self.__ensure_index_exists()

    def __ensure_index_exists(self):
        try:
            self.client.get_index(self.index_name)
        except MarqoWebError as e:
            if "IndexNotFound" in str(e):
                self.client.create_index(self.index_name, model=self.model)
            else:
                raise e

    def index_documents(self, docs: list):
        """
        Indexes a list of documents with specified tensor fields.
        """
        if not docs:
            return {"status": "No documents to index."}
        return self.client.index(self.index_name).add_documents(
            docs, tensor_fields=self.tensor_fields
        )

    def search(self, query: str, filter_string: str = None):
        return self.client.index(self.index_name).search(
            q=query, filter_string=filter_string
        )
