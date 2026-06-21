
import smtplib
from email.mime.text import MIMEText
from email.header import Header


res='test'
# 得到结果后，发送邮件给相关人员
# 第三方SMTP服务

# IMAP/SMTP 设置方法
# 用户名/帐户： 你的QQ邮箱完整的地址
# 密码： 生成的授权码
# 电子邮件地址： 你的QQ邮箱的完整邮件地址
# 接收邮件服务器： imap.qq.com，使用SSL，端口号993
# 发送邮件服务器： smtp.qq.com，使用SSL，端口号465或587

## 示例1
# mail_host = "smtp.163.com"
# mail_user = "jwjxlxl@163.com"
# mail_pass = "VWigDeCeNKgLjgst"
# mail_port = 25

# sender = "jwjxlxl@163.com"
# receivers = "1053851332@qq.com"

## 示例2
mail_host = "smtp.163.com"
mail_user = "m19854738982@163.com"
mail_pass = "EC974mVFMFzVzMxP"
mail_port = 25
sender = "m19854738982@163.com"
receivers = "1053851332@qq.com"




message = MIMEText(res ,'plain', 'utf-8')
message["from"] = sender
message["to"] = receivers

try:
    smtp = smtplib.SMTP()
    smtp.connect(mail_host, mail_port)
    smtp.login(mail_user, mail_pass)
    smtp.sendmail(sender, receivers, message.as_string())

    print("邮件发送成功")
except Exception as e:
    print(f"邮件发送失败{e}")