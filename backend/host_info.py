class SSHHost(object):
    def __init__(self,request):
        self.request = request
        self.ssh_connect()


    def ssh_connect(self):
        print("SSH_connect执行成功",self.request.user)
