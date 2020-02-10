#
# # EC2 Ubuntu 18.04
# 默认系统会提供3.6.8以上的版本，这个版本也可以正常使用，只是没有PIP,我们需要给python3,安装pip
# ls /usr/bin/python*ls /usr/bin/python*  查看系统上所有Python的命令
# # 安装 PIP3
# $ apt-get update
# $ sudo apt install python3-pip
# sqlite3已经安装好了，这省去了很多之前的怕坑工作。
# 所以直接安装项目所需的模块即可
# # 安装django所需模块
# $ pip3 install django
# $ pip3 install celery
# $ pip3 install paramiko
# $ pip3 install djangorestframework
# $ pip3 install markdown       # Markdown support for the browsable API.
# $ pip3 install django-filter  # Filtering support
# # 安装GIT 下载项目 系统已经安装好了git所以不需要继续安装
# $ cd /home
# # 系统如果以及安装了git就不需要在安装了，$ sudo apt-get install git
# # 查看版本git -- version
# $ ssh-keygen -t rsa -C luckygogreen@me.com
# $ more /root/.ssh/id_rsa.pub
# $ ssh -T git@github.com
# # 配置用户名
# $ git config --global user.name luckygogreen
# # 配置email
# $ git config --global user.email luckygogreen@me.com
# $ cd /home
# $ git clone https://github.com/luckygogreen/AccessGateway.git
# # 配置正确,测试是否安装成功
# $ cd /home/AccessGateway
# $ python3 manage.py runserver 0.0.0.0:9002
# 如果提示/bin/sh: 1: python: not found 错误，是因为没有指定系统版本，单独开启的进程文件无法运行
# 直接设置python3为默认系统版本即可
# $ update-alternatives --install /usr/bin/python python /usr/bin/python3 8
# $ sudo update-alternatives --config python    检查是否配置成功 提示There is only one alternative....就是成功了
