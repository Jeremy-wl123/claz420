import random
import numpy as np

# 1. 基础配置
DIM = 128  # 向量维度
docs = [
    "向量数据库用于存储文本、图片转化后的数值向量",
    "Milvus、Chroma、FAISS都是主流向量数据库",
    "RAG流程：文档向量化 -> 向量检索 -> 大模型拼接上下文回答",
    "余弦相似度用来衡量两个向量之间的相近程度",
    "分片存储可以提升向量数据库检索速度"
]

# 2. 生成随机向量（模拟embedding）
def gen_random_vector(dim=DIM):
    return np.random.uniform(-1, 1, dim)

# 3. 余弦相似度计算（相似度分数）
def cos_similarity(vec_a, vec_b):
    dot_product = np.dot(vec_a, vec_b)
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    score = dot_product / (norm_a * norm_b)
    return round(score, 4)

# 4. 构建向量知识库
vector_store = []
print("===== 文档向量化结果 =====")
for idx, text in enumerate(docs, 1):
    vec = gen_random_vector()
    vector_store.append({
        "content": text,
        "vector": vec
    })
    print(f"\n文档{idx}：{text}")
    print(f"对应向量数组：{vec.tolist()}")

# 5. 用户查询
query = "RAG完整执行步骤是什么"
query_vec = gen_random_vector()
print(f"\n===== 查询向量数组 =====")
print(query_vec.tolist())

# 6. 遍历库计算每一条的相似度分数
retrieve_list = []
for item in vector_store:
    sim_score = cos_similarity(query_vec, item["vector"])
    retrieve_list.append({
        "text": item["content"],
        "similarity_score": sim_score
    })

# 按相似度分数从高到低排序
retrieve_list.sort(key=lambda x: x["similarity_score"], reverse=True)
top3 = retrieve_list[:3]

# 打印带分数的检索结果
print("\n===== 检索结果（相似度分数）=====")
for idx, res in enumerate(top3, 1):
    print(f"{idx}. 相似度分数：{res['similarity_score']}")
    print(f"   文本：{res['text']}")

# 拼接上下文模拟大模型回答
context = "\n".join([f"【相似度{res['similarity_score']}】{res['text']}" for res in top3])
print("\n===== 结合检索上下文生成回答 =====")
prompt = f"""参考资料：
{context}
用户提问：{query}
请根据上面资料回答问题"""
print(prompt)
print("\n回答：RAG主要分为三步：文档向量化、向量相似度检索、依托检索到的文档上下文生成答案。")