from marqo import Client
from marqo.errors import MarqoWebError
from typing import List, Optional, Dict, Any
from more_itertools import chunked


class MarqoClient:
    def __init__(
        self,
        url: str,
        index_name: str,
        model: str = "hf/all-MiniLM-L6-v2",
        tensor_fields: Optional[List[str]] = None,
    ):
        self.client = Client(url)
        self.index_name = index_name
        self.model = model
        self.tensor_fields = list(set((tensor_fields or []) + ["text"]))
        self.__ensure_index_exists()

    def __ensure_index_exists(self):
        try:
            self.client.get_index(self.index_name)
            print(f"Index '{self.index_name}' already exists.")
        except MarqoWebError as e:
            if getattr(e, "code", None) == "index_not_found":
                self.client.create_index(self.index_name, model=self.model)
                print(f"Created index '{self.index_name}' with model '{self.model}'.")
            else:
                print(f"Unexpected error while checking index: {e}")
                raise

    def _clean_document(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        """Converts all non-dict values to strings (required by Marqo)."""
        return {k: (str(v) if v is not None else "") for k, v in doc.items()}

    def index_documents(self, docs: List[Dict[str, Any]], batch_size: int = 100):
        if not docs:
            return {"status": "No documents to index."}

        cleaned_docs = [self._clean_document(doc) for doc in docs]
        fields = self.tensor_fields or self._infer_tensor_fields(cleaned_docs)

        for batch in chunked(cleaned_docs, batch_size):
            try:
                self.client.index(self.index_name).add_documents(
                    batch, tensor_fields=fields
                )
            except Exception as e:
                print(f"Failed to index batch: {e}")
                continue

        return {"status": f"Indexed {len(cleaned_docs)} documents."}

    def _infer_tensor_fields(self, docs: List[Dict[str, Any]]) -> List[str]:
        """Infer tensor fields and ensure 'text' is always included."""
        example_doc = docs[0]
        candidate_fields = [
            k for k, v in example_doc.items() if isinstance(v, str) and k != "_id"
        ]
        if "text" not in candidate_fields:
            candidate_fields.append("text")
        return candidate_fields

    def search(
        self,
        query: str,
        filter_string: Optional[str] = None,
        searchable_attributes: Optional[List[str]] = None,
    ):
        return self.client.index(self.index_name).search(
            q=query,
            filter_string=filter_string,
            searchable_attributes=searchable_attributes,
        )
