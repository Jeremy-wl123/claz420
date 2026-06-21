import smtplib
from email.mime.text import MIMEText

res = "太子我爱你"   # 你的实际内容

mail_host = "smtp.qq.com"     # 官方指定
mail_port = 465
mail_user = "wolin105@qq.com"
mail_pass = "pingnllumhbzbceg"   # 注意：不是登录密码
sender = mail_user
receivers = "1367780968@qq.com"



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