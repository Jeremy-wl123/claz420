# Please install OpenAI SDK first: `pip3 install openai`
import os


from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=[
        {"role": "system", "content": "你是邮箱发送助手"},
        {"role": "user", "content": "帮我写一个100字表白情书"},
    ],
    stream=False,
    reasoning_effort="high",
    extra_body={"thinking": {"type": "enabled"}}
)

print(response.choices[0].message.content)
# print(response.choices[0].message)
# print(type(response.choices[0].message))

# with open('ds_output.json','w',encoding='utf-8') as f:
#     f.write(response.model_dump_json(indent=2, ensure_ascii=False)) # indent=2 缩进2格 调整格式

# import smtplib
# from email.mime.text import MIMEText
#
# res = response.choices[0].message.content   # 你的实际内容
#
# mail_host = "smtp.qq.com"     # 官方指定
# mail_port = 465
# mail_user = "wolin105@qq.com"
# mail_pass = "pingnllumhbzbceg"   # 注意：不是登录密码
# sender = mail_user
# receivers = "1367780968@qq.com"
#
#
#
# message = MIMEText(res, 'plain', 'utf-8')
# message["From"] = sender
# message["To"] = receivers
# message["Subject"] = "邮件主题"
#
# try:
#     smtp = smtplib.SMTP_SSL(mail_host, mail_port)
#     smtp.login(mail_user, mail_pass)
#     smtp.sendmail(sender, [receivers], message.as_string())
#     smtp.quit()
#     print("邮件发送成功")
# except Exception as e:
#     print(f"邮件发送失败: {e}")