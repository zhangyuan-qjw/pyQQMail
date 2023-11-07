import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from bs4 import BeautifulSoup
import os


# 读取HTML文件，并读取相应的保存数据，返回模板html，并删除本地记入的数据
def createTemplate(modelName):
    current_dir = os.getcwd()
    path = os.path.join(current_dir, "htmlTemplate", modelName, f"{modelName}.html")
    with open(path, "r", encoding="utf-8") as html_file:
        html_content = html_file.read()
    return html_content


# 构造邮件信息
def msg(html_content, receiver_email, subject, sender_email, modelName):
    # 使用Beautiful Soup解析HTML内容，提取所有img标签的src属性
    soup = BeautifulSoup(html_content, "html.parser")
    img_tags = soup.find_all("img")
    # 创建邮件对象
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    # 遍历所有img标签，将本地图片作为附件添加到邮件中
    for img in img_tags:
        img_src = img["src"]
        # 本地图片的文件路径
        current_dir = os.getcwd()
        image_path = os.path.join(current_dir, "htmlTemplate", modelName, img_src)
        if os.path.exists(image_path):
            with open(image_path, "rb") as img_file:
                image_data = img_file.read()
                image_mime = MIMEImage(image_data, name=os.path.basename(image_path))
                image_mime.add_header("Content-ID", f"<{img_src}>")
                msg.attach(image_mime)
                img.replace_with(soup.new_tag("img", src=f"cid:{img_src}"))
    # 将HTML内容添加到邮件对象中
    msg.attach(MIMEText(str(soup), "html"))
    return msg


def send(receiver_email, sender_email, subject, modelName):
    try:
        smtp_server = "smtp.qq.com"
        smtp_port = 587  # SMTP服务器的端口号（具体的端口号可以根据你的邮箱提供商设置而定）
        smtp_password = "lvtdbvkgxdpydead"

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # 使用TLS加密通信
        server.login(sender_email, smtp_password)
        template = createTemplate(modelName)  # html
        message = msg(template, receiver_email, subject, sender_email, modelName)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
    except Exception as e:
        # 这里需要记录日志
        print("邮件发送失败:", str(e))
