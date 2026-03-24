import chromadb
from sentence_transformers import SentenceTransformer

class ChromaIntegration:
    def __init__(self, model_name='sentence-transformers/all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.client = chromadb.Client()
        self.collection = self.client.create_collection(name='member_embeddings')

    def store_member_embedding(self, member_id, member_data):
        embedding = self.model.encode(member_data)
        self.collection.add(documents=[member_data], embeddings=[embedding], metadatas=[{'member_id': member_id}])

    def semantic_search(self, query, num_results=5):
        query_embedding = self.model.encode(query)
        results = self.collection.query(embeddings=[query_embedding], n_results=num_results)
        return results['documents'][0]

    def retrieve_member_by_id(self, member_id):
        results = self.collection.query(where={'member_id': member_id})
        return results['documents'][0] if results['documents'] else None

# Example usage
if __name__ == '__main__':
    chroma_integration = ChromaIntegration()
    example_member_id = '001'
    example_member_data = 'John Doe, a software engineer in AI.'

    # Store a member embedding
    chroma_integration.store_member_embedding(example_member_id, example_member_data)

    # Perform semantic search
    search_results = chroma_integration.semantic_search('software engineer')
    print('Search Results:', search_results)

    # Retrieve member by ID
    member_info = chroma_integration.retrieve_member_by_id(example_member_id)
    print('Member Info:', member_info)