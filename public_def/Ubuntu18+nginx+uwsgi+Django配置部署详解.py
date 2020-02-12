# # Ubuntu18.0.4 +Nginx+uwsgi+Django 服务器动静态部署
#
# # 安装uwsgi
# pip3 install uwsgi
# # 测试启动uwgi
# uwsgi --http 0.0.0.0:80 --file AccessGateway/wsgi.py --static-map=/static=statics   # statics一定是绝对路径
# #如果上面的测试成功，就需要手动创建一个uwsgi.ini的配置文件
# # 在项目里面
# mkdir script   # 创建一个script，然后cd 进入 目录方便日后管理
# vi uwsgi.ini   # 编辑配置文件
#
#
#
# #uwsgi 配置文件
# [uwsgi]
# #项目目录
# chdir=/home/AccessGateway
# #指定项目的application
# module=AccessGateway.wsgi:application
# #指定Sock的文件路径
# socket=/home/script/uwsgi.sock
# #进程个数
# processes = 5
# #worker个数
# workers=5
# #自动移除unix socket和pid文件，当服务停止的时候
# pidfile=/home/script/uwsgi.pid
# #配置IP端口
# http=0.0.0.0:9002  #  不能和nginx是同一个端口
# #指定静态文件
# static-map=/static=/home/AccessGateway/statics
# #启用uwsgi的用户名和用户组
# uid = root
# gid = root
# #启用主进程
# master = true
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
#
# 执行启动脚本，后期可以放入到启动任务里面
# 启动uwsgi  #需进到uwsgi.ini的文件目录下，例如：/home/script
# uwsgi --ini uwsgi.ini
# # 停止
# uwsgi --stop uwsgi.pid
# # 重载配置
# uwsgi --reload uwsgi.ini
# # 查看启动的uwsgi 进程
# ps -ef |grep uwsgi
# # 如果配置错误可以删掉文件夹目录的pid文件再启动一次
# rm -r -f uwsgi.pid
#
#################################################
# # 安装nginx
# apt-get update
# apt-get install nginx
# # 启动ngnix
# /etc/init.d/nginx start
# Nginx配置
# cd /etc/nginx/conf.d/   # 找到nginx路径
# vi AccessGateway.conf    # 创建一个你项目的conf文件
# server
# {
#     listen 80;
#     server_name www.cjkbg.com;
#     access_log/var/log/nginx/access.log;
#     charset utf-8;
#     gzip on;
#     gzip_types text/plain application/x-javascript text/css text/javascript application/x-httpd-php application/json text/json image/jpeg image/gif image/png image/jpg application/octet-stream;
#     error_page 404 /404.html
#     error_page 500 502 503 504 /50x.html
#     # root /var/www/html;
#     # index index.html index.htm index.nginx-debian.html;
#     location / {
#         include uwsgi_params;
#         uwsgi_connect_timeout 30;
#         uwsgi_pass unix: / home / script / uwsgi.sock;
#     }
#     location /static/ {
#         alias /home/AccessGateway/statics/;
#         index index.html index.htm;
#     }
#
# }
# # /etc/init.d/nginx restart   # 重启nginx服务器


#
# server {   # 这个server标识我要配置了
#         listen 80;
#         server_name 192.168.17.129;
#         access_log  /var/log/nginx/access.log;
#         charset  utf-8;
#         gzip on;
#         gzip_types text/plain application/x-javascript text/css text/javascript application/x-httpd-php application/json text/json image/jpeg image/gif image/png application/octet-stream;
#
#         error_page  404           /404.html;
#         error_page   500 502 503 504  /50x.html;
#
#         # 指定项目路径uwsgi
#         location / {        # 这个location就和咱们Django的url(r'^admin/', admin.site.urls),
#             include uwsgi_params;  # 导入一个Nginx模块他是用来和uWSGI进行通讯的
#             uwsgi_connect_timeout 30;  # 设置连接uWSGI超时时间
#             uwsgi_pass unix:/home/script/uwsgi.sock;  # 指定uwsgi的sock文件所有动态请求就会直接丢给他
#         }
#
#         # 指定静态文件路径
#         location /static/ {
#             alias  /home/trunk/static/;
#             index  index.html index.htm;
#         }

# Nginx无法启动或是出现错误可以通过下面的命令，查看错误信息
# systemctl status nginx.service