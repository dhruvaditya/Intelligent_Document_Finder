# initialize LLM + node parser
llm = OpenAI(model="gpt-4")
splitter = SentenceSplitter(chunk_size=1024)

nodes = splitter.get_nodes_from_documents(documents)
# initialize storage context (by default it's in-memory)
storage_context = StorageContext.from_defaults()
storage_context.docstore.add_documents(nodes)
index = VectorStoreIndex(
    nodes=nodes,
    storage_context=storage_context,
)
#BM25 retriever
# We can pass in the index, doctore, or list of nodes to create the retriever
retriever = BM25Retriever.from_defaults(nodes=nodes, similarity_top_k=2)
from llama_index.core.response.notebook_utils import display_source_node

# will retrieve context from specific companies
nodes = retriever.retrieve("What happened at Viaweb and Interleaf?")
for node in nodes:
    display_source_node(node)