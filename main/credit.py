import re
from tool.connect import insert

pattern = r'([\w.]+@[\w.]+)(T\d{4}U\d{2}D\d{1,2})'

tu = r'T(\d{4})U(\d{2})D(\d{1,2})'


# TU解析规则，并存入数据库
def TU(field, email, templateName, subject):
    result = re.search(tu, field)
    if result:
        T = result.group(1)
        U = result.group(2)
        D = result.group(3)
        date = T[:2] + "-" + T[2:]
        hour = U + ":00"
        number = int(D)
        isSuccess = insert('taskmail',
                           {'Date': date, 'Time': hour, 'Sendto': email, 'Template': templateName, 'Num': number,
                            'Subject': subject})
        if isSuccess:
            print('邮件预约成功！')
        else:
            print('邮件预约失败！请确保格式正确，如有问题请发送邮件到2921572176@qq.com!')


def parse(templateList):
    if templateList:
        print(templateList)
        for work in templateList:
            modelName = work['path']
            match = re.search(pattern, work['to'])
            if match:
                email = match.group(1)
                t_field = match.group(2)
                TU(t_field, email, modelName, work['name'])
            else:
                print('邮件预约失败！请确保格式正确，如有问题请发送邮件到2921572176@qq.com!')
