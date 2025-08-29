from langchain_huggingface import HuggingFaceEmbeddings


class Embeddings:
    def load_model(self):
        embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        return embeddings_model
