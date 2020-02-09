
# EC2 Ubuntu 18.04   升级python 3.8.1 最正确的方式
# 第一步更新
$ apt-get update
# 第二步输入python看看是否有python
# 如果没有
$ apt install python
# 这时候输入python 和python3 就可以查看到各自的版本
# python 2.7.17
# python3 3.6.8
# 为了不冲突，我直接全部删除3.6.8
$ sudo apt-get remove python3.6
$ sudo apt-get remove --auto-remove python3.6
$ sudo apt-get purge python3.6
$ sudo apt-get purge --auto-remove python3.6
# 此时再次看一下是不是有没删除干净的
# $ whereis python3
# 找到后全部删除
# rm -r -f 删除
$ rm -r -f /usr/lib/python3
$ rm -r -f /usr/lib/python3.6
$ rm -r -f /etc/python3
$ rm -r -f /etc/python3.6

# 然后开始安装python
# 官网下载最新python 3.8.1
$ wget https://www.python.org/ftp/python/3.8.1/Python-3.8.1.tgz
# 解压
$ tar -xvzf Python-3.8.1.tgz
# 安装依赖
$ sudo apt-get update
$ sudo apt-get upgrade
$ sudo apt-get dist-upgrade
# 如果出现选中mainlist 选中第一个
$ sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev
# 进入文件包
$ cd Python-3.8.1
# 编译
$ ./configure --prefix=/usr/local/python3
# 安装
$ make && make install
# 删除软链接
$ sudo rm -rf /usr/bin/python3
$ sudo rm -rf /usr/bin/pip3
# 新建软链接
$ sudo ln -s /usr/local/python3/bin/python3.8 /usr/bin/python3
$ sudo ln -s /usr/local/python3/bin/pip3.8 /usr/bin/pip3

# 填坑安装sqlite3
# 查看目前sqlite3的安装位置
# $ find / -name _sqlite3.so
# 发现在/usr/local/python3/lib/python3.8/lib-dynload/这个路径下没找到_sqlite3.so
# 下载安装包:
$ wget https://www.sqlite.org/2018/sqlite-autoconf-3240000.tar.gz
# 解压：
$ tar -xvzf sqlite-autoconf-3240000.tar.gz
# 进入目录:
$ cd sqlite-autoconf-3240000/
# 编译:
$ ./configure --prefix=/usr/local/sqlite
# 安装 ：make -j4&&sudo make install
# 进入python3安装目录
$ cd ~/Python-3.8.1
# 修改setup.py
$ vi setup.py
# 查找" sqlite_inc_paths"  最下方新增
# '/usr/local/sqlite/include'
# '/usr/local/sqlite/include/sqlite3'
# 编译python3
$ ./configure --enable-loadable-sqlite-extensions
# 重装python3
$ make && sudo make install

# 升级pip
$ pip3 install --upgrade pip
$ sudo apt-get install python3-pip
# 安装django所需模块
$ pip3 install django
$ pip3 install celery
$ pip3 install paramiko
$ pip3 install djangorestframework
$ pip3 install markdown       # Markdown support for the browsable API.
$ pip3 install django-filter  # Filtering support
# 安装GIT
$ cd /home
$ sudo apt-get install git
$ ssh-keygen -t rsa -C luckygogreen@me.com
$ more /root/.ssh/id_rsa.pub

$ ssh -T git@github.com
$ git clone https://github.com/luckygogreen/AccessGateway.git

# python版本管理软件
# 列出所有的版本编号，如果没有需要配置
$ update-alternatives --list python
# 配置python2.7 是1  数字越大，权限越高，就是默认要执行的  python 就是要配置的名字
$ update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1
# 配置python3 是2
$ update-alternatives --install /usr/bin/python python /usr/local/bin/python3 2
# 再次查看
$ update-alternatives --list python
#   Selection    Path                    Priority   Status
# ------------------------------------------------------------
# * 0            /usr/local/bin/python3   2         auto mode
#   1            /usr/bin/python2.7       1         manual mode
#   2            /usr/local/bin/python3   2         manual mode
# 配置正确,测试是否安装成功
$ cd /home/AccessGateway
$ python3 manage.py runserver 0.0.0.0:9002
