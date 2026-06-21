from fastapi import FastAPI
from pydantic import BaseModel, Field
import smtplib
from email.mime.text import MIMEText

# 邮件配置
mail_host = "smtp.qq.com"
mail_port = 465
mail_user = "wolin105@qq.com"
mail_pass = "pingnllumhbzbceg"   # 注意：不是登录密码
sender = mail_user

def send_email(res='test', receivers='1053851332@qq.com'):
    """
    发送邮件函数
    - 如果调用时不传参数，使用默认值
    """
    message = MIMEText(res, 'plain', 'utf-8')
    message["From"] = sender
    message["To"] = receivers
    message["Subject"] = "邮件主题"

    try:
        smtp = smtplib.SMTP_SSL(mail_host, mail_port)
        smtp.login(mail_user, mail_pass)
        smtp.sendmail(sender, [receivers], message.as_string())
        smtp.quit()
        print("邮件发送成功")
    except Exception as e:
        print(f"邮件发送失败: {e}")

app = FastAPI()

# 定义请求体模型（带默认值）
class EmailRequest(BaseModel):
    res: str = Field(default='test', description="邮件内容")
    receivers: str = Field(default='1053851332@qq.com', description="收件人邮箱地址")

@app.post("/send_email")
async def send_email_endpoint(email_req: EmailRequest):
    """
    发送邮件接口
    - 如果不传 res 或 receivers，使用默认值
    """
    send_email(email_req.res, email_req.receivers)
    return {"message": "邮件发送成功"}

@app.get('/health')
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
