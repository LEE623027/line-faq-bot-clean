from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

INDEX_DIR = "faiss_index"

def query_knowledge(query_text):
    try:
        embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        db = FAISS.load_local(INDEX_DIR, embedding_model, allow_dangerous_deserialization=True)
        results = db.similarity_search(query_text, k=3)
        return [r.page_content for r in results]
    except Exception as e:
        print("[ERROR] 查詢錯誤：", str(e))
        return []
