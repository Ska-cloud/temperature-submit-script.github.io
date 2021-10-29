# -*- coding: utf-8 -*-
"""
@Description :
@Time ： 2021/10/14 8:45 下午
@Auth ： Ska
@File ：temperature_demo.py
@IDE ：PyCharm

"""
import datetime
import time
import os
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.options import Options
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import random
import schedule
import threading


# 校园网登陆，体温填写
def chrome_submit(user, pwd):
    # 实例化无可视化界面操作
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    # 实现规避检测
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])

    driver = webdriver.Chrome('./chromedriver', options=option, chrome_options=chrome_options)

    driver.implicitly_wait(10)  # 若执行find操作时，响应慢没有查到元素，不会立即抛出异常，会等待半秒继续执行find操作
    url = 'https://web-vpn.sues.edu.cn/'
    # 进入学校网页VPN登陆界面
    driver.get(url)
    # 定位用户名输入框
    driver.find_element_by_id('username').send_keys(user)
    # 定位密码输入框
    location1 = driver.find_element_by_id('password')
    location1.send_keys(pwd)
    time.sleep(2)   # 模拟真实登陆
    # 回车
    location1.send_keys(Keys.ENTER)

    # 点击进入健康体温填报系统
    driver.find_element_by_class_name('vpn-content-block-panel').click()

    # 跳转页面填写体温
    driver.switch_to.window(driver.window_handles[1])
    temperature = str(round(random.uniform(36, 37), 1))
    # 定位到提问填写输入框
    location2 = driver.find_element_by_xpath('//*[@id="form"]/div[18]/div[1]/div/div[2]/div/div/input')
    location2.clear()
    time.sleep(2)  # 模拟真实登陆
    location2.send_keys(temperature)
    driver.find_element_by_id('post').click()
    time.sleep(2)  # 模拟真实登陆
    driver.quit()


# 填报完成发送邮件
def send_mail(content):
    my_sender = 'xxxx@qq.com'  # 发件人邮箱账号
    my_pass = 'cxundcibsrwbcgj'  # qq邮箱stmp授权码
    my_user = 'xxxx@qq.com'  # 收件人邮箱账号，我这边发送给自己

    try:
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['From'] = formataddr(["Ska", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["sb", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "体温填报"  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接

        print('*' * 60)
        print("邮件发送成功")
        print('*' * 60)
    except Exception as e:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        print('*' * 60)
        print("邮件发送失败")
        print('*' * 60)


# 体温填报
def submit_temperature(name, pwd):
    now_hour = time.strftime('%H')
    now_data = datetime.datetime.now().strftime('%Y') + '年' + datetime.datetime.now().strftime('%m') + '月' + datetime.datetime.now().strftime('%d') + '日'
    # 上午体温填报
    if 7 <= int(now_hour) <= 12:
        if not os.path.exists(str(name) + ' ' + str(now_data) + '上午.txt'):

            try:
                chrome_submit(name, pwd)
                with open(str(name) + ' ' + str(now_data) + '上午.txt', 'w', encoding='utf-8') as fp:
                    text = str(name) + ' ' + str(now_data) + '上午体温填报成功'
                    fp.write(text)
            except Exception as e:
                text = str(name) + ' ' + str(now_data) + '上午体温填报失败'

            send_mail(text)     # 发送邮件

    # 下午体温填报
    if 13 <= int(now_hour) <= 17:
        if not os.path.exists(str(name) + ' ' + str(now_data) + '下午.txt'):
            try:
                chrome_submit(name, pwd)
                with open(str(name) + ' ' + str(now_data) + '下午.txt', 'w', encoding='utf-8') as fp:
                    text = str(name) + ' ' + str(now_data) + '下午体温填报成功'
                    fp.write(text)
            except Exception as e:
                text = str(name) + ' ' + str(now_data) + '下午体温填报失败'

            send_mail(text)  # 发送邮件


def read_json_config(name, path):
    with open(path, 'r') as f:
        config_list = json.load(f)
        username = config_list[name][0]['username']
        password = config_list[name][1]['password']

    return username, password


# 用户1的线程
def job1():
    print('user1 threading is running.....')
    print('-' * 60)
    username, password = read_json_config('user1', './config.json')
    submit_temperature(username, password)
    print('user1 threading was finished.....')
    print('-' * 60)


# 用户2的线程
def job2():
    print('user2 threading is running.....')
    print('-' * 60)
    username, password = read_json_config('user2', './config.json')
    submit_temperature(username, password)
    print('user2 threading was finished.....')
    print('-' * 60)


def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


if __name__ == '__main__':
    schedule.every(10).miniutes.do(run_threaded, job1)
    schedule.every(10).minuutes.do(run_threaded, job2)
    # 执行schedule
    while True:
        schedule.run_pending()




