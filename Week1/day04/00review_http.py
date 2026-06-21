# 请求行（Request Line）
# 描述请求方法、目标资源路径和HTTP协议版本。
#
# 请求头（Headers）
# 一组键值对，用于传递附加信息（如认证、数据格式、缓存策略等）。
#
# 请求体（Body，可选）
# 携带实际数据，常用于POST、PUT等需要提交内容的请求。


# 示例

# POST / chat / completions HTTP / 1.1          ← 请求行
# Host: api.deepseek.com

# Content - Type: application / json            ← 请求头
# Authorization: Bearer sk - xxxxxx
#
# {"model": "deepseek-v4-pro", ...}             ← 请求体（JSON格式）