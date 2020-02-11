# #uwsgi 配置文件
# [uwsgi]
# #项目目录
# chdir = /home/AccessGateway
# #指定项目的application
# module=teacher.wsgi:application
# #指定Sock的文件路径
# socket=base = /home/script/uwsgi.sock
# #进程个数
# processes = 5
# #worker个数
# workers=5
# pidfile=/home/script/uwsgi.pid
# #指定静态文件
# static-map=/static=/home/AccessGateway/statics
# #启用uwsgi的用户名和用户组
# uid = root
# gid = root
# #启用主进程
# master = true
# #自动移除unix socket和pid文件，当服务停止的时候
# vacuum=true
# #序列化接受的内容，如果可能的话
# thunder-lock=true
# #启用线程
# enable-threads=true
# #设置自中断时间
# harakiri=30
# #设置缓存
# post-buffering=4096
# #设置日志
# daemonize=/home/script/uwsgi.log
# #
# #
# # # base = /home/AccessGateway
# # # file = /home/AccessGateway/AccessGateway/wsgi.py
# #
# /etc/init.d/nginx restart   # 重启nginx服务器
# uwsgi --ini uwsgi.ini  启动uwsgi  #需进到uwsgi.ini的文件目录下，例如：/home/script