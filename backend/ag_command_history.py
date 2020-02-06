from Web import models
from django import conf
from public_def import all_about_json


class CommandHistory(object):
    def __init__(self, request):
        self.request = request
        self.get_command_history()

    def get_command_history(self):
        print("执行get_command_history成功")
        command_task = models.UserProfile.objects.get(id=self.request.user.id).host_to_remote_users.select_related()
        command_history_list = []
        for i in command_task.order_by('-id'):
            task_details = i.taskdetails_set.select_related()
            for j in task_details:
                if j.result == '':
                    result = 'Runs successfully with no results'
                else:
                    result = j.result
                if j.task.tasktype == 'filetrans':
                    command = 'File Upload'
                else:
                    command = j.task.taskcontent
                command_dict = {
                    'id': j.id,
                    'type': j.task.tasktype,
                    'command': command,
                    'status': j.get_status_display(),
                    'result': j.result,
                    # 'result': html_cmd_result1,
                    'hostname': j.host_to_remote_user.host.name,
                    'hostip': j.host_to_remote_user.host.ip_addr,
                    'date': j.data.strftime("%Y-%m-%d %H:%I:%S")
                }
                command_history_list.append(command_dict)
        self.command_history_list = command_history_list
        dir_path = "%s/statics/data/%s/" % (conf.settings.BASE_DIR,self.request.user.id)
        file_path = "%s/statics/data/%s/command_history.json" % (conf.settings.BASE_DIR,self.request.user.id)
        all_about_json.write_json_file(dir_path, file_path, self.command_history_list) # 调用写入json方法
    # def write_command_history_to_json(self):
    #     with open("%s/statics/data/command_history.json" % conf.settings.BASE_DIR, "w") as f:
    #         json.dump(self.command_history_list, f)
    #         print("command_history_dict has been successfully written to a json file[/data/command_history.json]")
