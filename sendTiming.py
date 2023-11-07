import schedule
import yaml
from datetime import datetime, timedelta
from tool.connect import query
from main.send import send
import time
import queue
import threading
from functools import partial
from tool.logging import setup_logger

queue_mail = queue.Queue()  # 每一天的任务集合
with open('config.yaml', 'r', encoding='utf-8') as f:
    disposition = yaml.load(f.read(), Loader=yaml.FullLoader)

time_logger = setup_logger('logs/time.log')

sender_mail = disposition['login_qq']


def daily_task():
    try:
        # today加一天
        next_day = time.strftime("%m-%d", time.localtime(time.time() + 24 * 60 * 60))
        mail_list = query(next_day)
        if mail_list:
            for mail in mail_list:
                queue_mail.put(mail)
        create_mailTask()
    except Exception as e:
        time_logger.error(e)


def schedule_task(hour, receiver_email, sender_email, subject, modelName):
    now = datetime.now()
    target_time = now.replace(hour=hour, minute=0, second=0, microsecond=0) + timedelta(days=1)
    # 计算时间间隔
    time_until_target = target_time - now
    partial_send = partial(send, receiver_email, sender_email, subject, modelName)
    thread_schedule = schedule.Scheduler()
    thread_schedule.every(time_until_target.seconds).seconds.do(partial_send)
    time_logger.info(f"{subject}邮件已创建，待发送至{receiver_email}")
    while True:
        thread_schedule.run_pending()
        if datetime.now() >= target_time:
            schedule.clear()
            time_logger.info(f"{subject}邮件发送完毕，{receiver_email}已接收！")
            break
        time.sleep(1)


def create_mailTask():
    threads = []
    while not queue_mail.empty():
        mail = queue_mail.get()
        params = (int(mail['Time'][:2]), mail['Sendto'], sender_mail, mail['Subject'], mail['Template'])
        thread = threading.Thread(target=schedule_task, args=params)
        threads.append(thread)
        thread.start()
    if threads:
        for thread in threads:
            thread.join()


main_schedule = schedule.Scheduler()
main_schedule.every().day.at("23:55").do(daily_task)
while True:
    main_schedule.run_pending()
    time.sleep(1)
