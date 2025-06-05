import os
import pandas as pd
import pickle
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain_huggingface import HuggingFaceEmbeddings

# 路徑設定（統一與 query.py 相同）
EXCEL_PATH = "SOP_知識庫建構模板.xlsx"
INDEX_FILE = "faiss_index"     # 儲存向量資料夾
DOCS_FILE = "docs.pkl"         # 儲存原始文件資料

# 讀取 Excel
df = pd.read_excel(EXCEL_PATH)

# 資料轉換
docs = []
for _, row in df.iterrows():
    category = str(row.get("分類", "")).strip()
    issue = str(row.get("常見問題", "")).strip()
    context = str(row.get("情境描述（選填）", "")).strip()
    solution = str(row.get("標準作法或建議對策", "")).strip()
    reference = str(row.get("參考文件/頁數", "")).strip()
    remark = str(row.get("備註", "")).strip()

    content = f"""分類：{category}
常見問題：{issue}
情境描述：{context}
標準作法或建議對策：{solution}
參考文件/頁數：{reference}
備註：{remark}"""

    metadata = {"分類": category, "常見問題": issue}
    docs.append(Document(page_content=content, metadata=metadata))

# 建立向量庫
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = FAISS.from_documents(docs, embedding_model)

# 儲存向量庫
db.save_local(INDEX_FILE)
with open(DOCS_FILE, "wb") as f:
    pickle.dump(docs, f)

print("✅ 知識庫建構完成！共建立 %d 筆資料。" % len(docs))
print(f"📂 向量庫已儲存在：{INDEX_FILE}")
