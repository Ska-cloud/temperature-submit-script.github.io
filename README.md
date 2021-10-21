# temperature-submit-script.github.io
上海工程技术大学VPN登录体温登记脚本
## 环境准备
python = 3.8
selenium = 3.141.0
lxml = 4.6.4
schedule = 1.1.0

pip、conda安装都可以
以conda为例说明：
‘’‘
conda create --name temperature python=3.8   # 创建名为temperature的虚拟环境
conda activate temperature
conda install selenium
conda install lxml
conda install schedule    # 有可能下载不了，下载不了用pip install
’‘’

## 其它准备
1、qq邮箱stmp服务如何设置自行百度，需要获取stmp授权码
2、准备chromedriver，文件里自带的chromedriver为unix版本，Mac用户可以直接用
Linux、Windows用户都可以直接去官网下载，建议Google Chrome和chromedriver都直接下载最新版本
因为需要版本对应，将下载好的chromedriver放到脚本文件里就可以

---
## 代码使用说明
1、此代码模拟学校vpn登录界面，不用担心必须要用vpn填写体温的情况
2、此代码可以创建多个job()为不同的人提供脚本自动填写功能，如果只有一个用户只需删除掉多的那个job即可
3、config.json文件需要自行填写，user1、user2字段只是为了区分不同用户，填什么无所谓只要不一样就可以了
但是填写的字段需要对应于read_json_config(name, path)中的name来提取用户名和密码

## 部署代码
‘’‘
cd xx/xx/xx/temperature-submit-script
conda ativate temperature 
python temperature_demo.py
’‘’
