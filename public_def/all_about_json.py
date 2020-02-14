import os, json


# 生成json文件
def write_json_file(dir_path, file_path, result_list):
    """
    :param dir_path: 文件目录 example:   dir_path = "%s/statics/data/public/" % conf.settings.BASE_DIR
    :param file_path: 文件绝对路径  example:  file_path = "%s/statics/data/public/timezone.json" % conf.settings.BASE_DIR
    :param result_list: 要写入的数据列表
    :return:
    """
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            json.dump(result_list, f)
            print("Successfully written to a json file[%s]" % file_path)
    else:
        with open(file_path, "w") as f:
            json.dump(result_list, f)
            print("Successfully written to a json file[%s]" % file_path)
