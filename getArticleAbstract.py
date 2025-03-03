# 目前您的用户等级是 Free，账号下的请求限制参考下方内容，如需扩容请查看
# 充值与限速的具体说明
# 并发数 1
# TPM32000
# RPM3
# TPDunlimited
# 因此每次循环至少等待 20s，最好 30s

from openai import OpenAI
import os, time

client = OpenAI(
    api_key="sk-kGqFhf86lWHjbpSZcdmeZfsc8hGei70oLCX9io7c44kAKR64",  # 在这里将 MOONSHOT_API_KEY 替换为你从 Kimi 开放平台申请的 API Key
    base_url="https://api.siliconflow.cn/v1", 
)

# 清空文件内容 
if os.path.exists("Abstract.txt"):
    os.remove("Abstract.txt")

# article_set = os.listdir("content/post")[11:]
# 需要生成的文章放在这
article_set = ["", ""]

for article in article_set:

    print(article + ":\n")

    with open(
        r"content/post/" + article + "/index.md", "r", encoding="utf-8"
    ) as file:  # 使用 UTF-8 编码打开文件
        content = file.read()  # 将文件内容读取为字符串

        completion = client.chat.completions.create(
            model='deepseek-ai/DeepSeek-V2.5',
            messages=[
                {
                    "role": "system",
                    "content": "你是一位文档总结助手，你会将我接下来发给你的 markdown 文章提取出一份小于 100 字的简要说明。",
                },
                {"role": "user", "content": content},
            ],
            temperature=0.3,
        )

    # 通过 API 我们获得了 Kimi 大模型给予我们的回复消息（role=assistant）
    print(completion.choices[0].message.content)

    # 打开文件并以追加模式写入内容
    with open(r"Abstract.txt", "a", encoding="utf-8") as file:  # 使用追加模式 'a'
        file.write(
            article + "\n\n" + completion.choices[0].message.content + "\n\n"
        )  # 写入内容

    time.sleep(30)
