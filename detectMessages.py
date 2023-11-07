import imapclient
import time
import pyzmail
from email.header import decode_header
import yaml
from main.credit import parse
from tool.logging import setup_logger

with open('config.yaml', 'r', encoding='utf-8') as f:
    disposition = yaml.load(f.read(), Loader=yaml.FullLoader)

detect_logger = setup_logger('logs/detect.log')

# QQ邮箱的IMAP服务器地址和端口号
imap_server = 'imap.qq.com'
imap_port = 993

# QQ邮箱账号和授权码
email = disposition['login_qq']
password = disposition['authorization_code']
templates = disposition['template']


# 创建并连接数据库


def isTemplates(name):
    for templateName in templates:
        if name == templateName['name']:
            return templateName['path']
    return ''


# 监听新邮件
while True:
    try:
        # 连接到QQ邮箱的IMAP服务器
        client = imapclient.IMAPClient(imap_server, use_uid=True)
        client.login(email, password)
        client.select_folder('INBOX', readonly=True)
        # 获取新邮件的UID（唯一标识符）
        new_mail_uids = client.search(['NEW'])
        new_mail = []
        # 遍历新邮件的UID，获取主题和内容
        for uid in new_mail_uids:
            raw_message = client.fetch([uid], ['BODY[]', 'FLAGS'])
            message = pyzmail.PyzMessage.factory(raw_message[uid][b'BODY[]'])
            subject, encoding = decode_header(message.get_subject())[0]
            # sender_name, sender_email = message.get_address('from')
            # 获取邮件内容
            path = isTemplates(subject)
            if not path:
                client.set_flags(uid, [b'\\Seen'])
                continue
            if message.text_part:
                mail_content = message.text_part.get_payload().decode(message.text_part.charset)
            elif message.html_part:
                mail_content = message.html_part.get_payload().decode(message.html_part.charset)
            else:
                mail_content = None
            client.set_flags(uid, [b'\\Seen'])
            new_mail.append({
                'path': path,
                'name': subject,
                'to': mail_content
            })
            client.logout()
            # 提取并记入
            parse(new_mail)
            detect_logger.info("New mail: {} from {}. Content: {}".format(subject, email, mail_content))
            time.sleep(5)
    except Exception as e:
        detect_logger.error("Error occurred: {}. Reconnecting...".format(e))
        time.sleep(10)  # 等待一段时间再尝试重连
        continue
