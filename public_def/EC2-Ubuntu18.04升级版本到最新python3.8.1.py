#
# # EC2 Ubuntu 18.04 升级到python3.8.1最好用方法
# 默认系统会提供3.6.8以上的版本，这个版本也可以正常使用，只是没有PIP,我们需要给python3,安装pip
# ls /usr/bin/python*ls /usr/bin/python*  查看系统上所有Python的命令
# # 安装 PIP3
# $ apt-get update
# $ sudo apt install python3-pip
# sqlite3已经安装好了，这省去了很多之前的怕坑工作。
# 开始升级Python3.8.1
# $ sudo apt update
# $ sudo apt install software-properties-common
# $ sudo add-apt-repository ppa:deadsnakes/ppa
# 出现提示时，按Enter继续
# 3、启用存储库后，请使用以下命令安装Python 3.8：
# $ sudo apt install python3.8
# 4、通过键入以下命令验证安装是否成功：
# $ python3.8 --version
# 返回信息：
# Python 3.8.1
# 至此，Python 3.8已安装在Ubuntu 18.04系统上，你可以开始使用它了。
# 给系统配置python版本的优先级，这个时候系统上应该有2到3个python版本， 最后的数字越大优先级越高
# $ sudo update-alternatives --config python    检查是否配置成功 提示There is only one alternative....就是成功了
# $ update-alternatives --install /usr/bin/python python /usr/bin/python3 8
# $ update-alternatives --install /usr/bin/python python /usr/bin/python3.8 9
# 运行python3 就是python3.6版本
# 运行python3.8或者直接运行python 就是python3.8版本
# 此时，pip3对应的库，却只是3.6的，pip3只能对应一个库，以后运到哪个库就修改下面的代码
# $ vi /usr/bin/pip3
# 修改第一行
#!/usr/bin/python3.8      （ 如果要用3.6版本 就改为python3 ,因为python对应3.6）
# pip3库不是公用的，如果切换默认版本到3.6，还需要重新安装一次pip3库，但是sqlite3不需要安装了
# # 安装程序运行所需模块
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


# 切换版本必须要完成两部操作
# 1，alternatives 更换默认版本，该数字即可
# 2，vi /usr/bin/pip3 默认指向