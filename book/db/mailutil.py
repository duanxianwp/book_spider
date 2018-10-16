import smtplib
from email.header import Header
from email.mime.text import MIMEText

from book import settings


def push_email(recieve_email, message):
    try:
        host = settings.EMAIL_URL
        port = settings.EMAIL_PORT
        user = settings.EMAIL_USER
        password = settings.EMAIL_PASSWORD
        mail_content = message
        mail_title = '新书快讯'

        msg = MIMEText(mail_content, "html", 'utf-8')
        msg["Subject"] = Header(mail_title, 'utf-8')
        msg["From"] = user
        msg["To"] = Header("被选召的孩子们", 'utf-8')

        smtp = smtplib.SMTP(host=host, port=port)
        smtp.ehlo(host)
        smtp.login(user, password)

        smtp.send_message(msg, user, recieve_email)
        smtp.quit()
        return True
    except Exception as e:
        print("failed,Exception:")
        print(e)
        return False