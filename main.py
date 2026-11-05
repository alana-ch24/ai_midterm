import os
from pydantic import BaseModel
from openai import OpenAI

# 1. 結構化輸出設定 (對應作業要求)：強迫 AI 只能回傳我們規定的格式
class EmailClassification(BaseModel):
    category: str
    confidence: float

# 2. 準備一封測試用的客訴信
sample_email = "我昨天買的吹風機今天就壞了，根本吹不出熱風，請立刻幫我換一台新的！"
print(f"收到信件內容：{sample_email}")
print("正在請 AI 分類中...\n")

# 3. 呼叫 AI 模型 (注意：這裡不會寫出金鑰，非常安全！)
client = OpenAI() # 它會自動去我們之後設定的保險箱拿密碼

try:
    # 這裡我們請 OpenAI 幫忙看信件
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "你是一個專業的客服信件分類員。請將信件分類為：'退貨'、'報修'、或'抱怨'。"},
            {"role": "user", "content": sample_email}
        ],
        response_format=EmailClassification, # 啟動結構化輸出
    )

    # 4. 印出 AI 整理好的結果
    result = response.choices[0].message.parsed
    print("=== AI 分類結果 ===")
    print(f"分類判定：{result.category}")
    print(f"AI 信心水準：{result.confidence}")

except Exception as e:
    print(f"發生錯誤了，請檢查設定：{e}")
