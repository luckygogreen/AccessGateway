//程序运行先执行的方法
active_menu()


// 全选反选  单组复选框
function checkall(selectStatus) {
    //传入参数（全选框的选中状态）
    //根据name属性获取到单选框的input，使用each方法循环设置所有单选框的选中状态
    if (selectStatus) {
        console.log(selectStatus)
        $("input[name='selectitem']").each(function (i, n) {
            n.checked = true;
        });
    } else {
        console.log(selectStatus)
        $("input[name='selectitem']").each(function (i, n) {
            n.checked = false;
        });
    }
}

// 全选反选  多组复选框
function groupcheckall(selectStatus, checkboxname) {
    if (selectStatus) {
        var allvalue = document.getElementsByName(checkboxname);
        for (var i = 0; i < allvalue.length; i++) {
            if (allvalue[i].type == "checkbox")
                allvalue[i].checked = true;
        }
    } else {
        var allvalue = document.getElementsByName(checkboxname);
        for (var i = 0; i < allvalue.length; i++) {
            if (allvalue[i].type == "checkbox")
                allvalue[i].checked = false;
        }
    }
}

//弹出窗口
function windowsopen(iip, iport) {
    window.open("http://" + iip + ":" + iport + "/", "_blank", "height:500,resizable=yes,width=600,top=10,left=10,toolbar=no,menubar=no,scrollbars=no,location=no,status=no");
//     window.open 弹出新窗口的命令；
// 　　'page.html' 弹出窗口的文件名；
// 　　'newwindow' 弹出窗口的名字（不是文件名），非必须，可用空''代替；
// 　　height=100 窗口高度；
// 　　width=400 窗口宽度；
// 　　top=0 窗口距离屏幕上方的象素值；
// 　　left=0 窗口距离屏幕左侧的象素值；
// 　　toolbar=no 是否显示工具栏，yes为显示；
// 　　menubar，scrollbars 表示菜单栏和滚动栏。
// 　　resizable=no 是否允许改变窗口大小，yes为允许；
// 　　location=no 是否显示地址栏，yes为允许；
// 　　status=no 是否显示状态栏内的信息（通常是文件已经打开），yes为允许；
}

//文件上传类型控制
function change_filetype_select(ele) {
    if ($(ele).val() == "getfrom") {
        $("#local_file_input").attr("class", "input-group mar-btm hidden")
    } else {
        $("#local_file_input").attr("class", "input-group mar-btm")
    }
}

//停止批量执行命令
function stop_shell_cmd(self) {
    $("#show_cmd_result").attr("class", " panel panel-bordered-primary hidden ");    //隐藏运行结果框
    $("#run_cmd_button").attr('disabled', false);        //程序运行过程中禁止提交执行按钮
    clearInterval(ResultRefresh);    //停止没有运行完的ajax循环获取数据操作
}

//停止文件执行命令
function stop_shell_file(self) {
    $("#show_cmd_result").attr("class", " panel panel-bordered-primary hidden ");    //隐藏运行结果框
    $("#run_file_button").attr('disabled', false);        //程序运行过程中禁止提交执行按钮
    clearInterval(ResultRefresh);    //停止没有运行完的ajax循环获取数据操作
}

//处理提交的CMD命令
function run_shell_cmd(self) {
    $("#show_host_results").text("")           //重新点击按钮后，清空之前的运行结果
    cmd_text = $("#cmdtext").val();      //获取CMD命令内容
    var select_host_ids = [];
    $("[tag='host_select']:checked").each(
        function () {
            select_host_ids.push($(this).val())
        }
    )
    if (select_host_ids.length == 0) {
        $.niftyNoty({
            type: 'pink',
            container: '#select_host_pannel',
            html: '<div class="media">🙁Please select a host and try again！</div>',
            closeBtn: true,
            timer: 2000
        });
    } else if (cmd_text.length <= 1) {
        $.niftyNoty({
            type: 'pink',
            container: '#cmd_pannel',
            html: '<div class="media">🙁Please try to enter a valid command！</div>',
            closeBtn: true,
            timer: 2000
        });
    } else {
        var task_mgr = {
            'select_host_ids': select_host_ids,
            'task_type': 'cmd',
            'cmd_text': cmd_text
        };


        $(self).attr("disabled", "true");  //程序运行过程中禁止提交执行按钮
        $("#show_cmd_result").attr("class", " panel panel-bordered-primary ");    //显示运行结果框
        var csrftoken = $("input[name='csrfmiddlewaretoken']").val()
        $.post("/batch_task_mgr/", {
            'task_data': JSON.stringify(task_mgr),
            'csrfmiddlewaretoken': csrftoken
        }, function (callback) {
            console.log("task_callback:" + callback)
            var callbackdata = JSON.parse(callback);
            $.each(callbackdata.select_host_list, function (index, ele) {
                console.log("ele:" + ele.host_to_remote_user__host__ip_addr)
                var li_ele = "<div pannelbox_id='" + ele.id + "' class=\"panel panel-bordered panel-dark \"><div class=\"panel-heading\"> <div class=\"panel-control\"> <div progressmain_id='" + ele.id + "' class=\"progress progress-md\" > <div progress_id='" + ele.id + "' style=\"width: 25%\" class=\"progress-bar progress-bar-primary progress-bar-striped active\"></div></div><button statusbutton_id='" + ele.id + "' class=\"btn btn-primary btn-labeled\" ><i statusi_id='" + ele.id + "' class=\"btn-label fa fa-gears\"  style=\" padding-left: 10px; border-left-width: 10px; \"></i> <span statusspan_id='" + ele.id + "'>Running</span></button></div><h3 class=\"panel-title\">" + (index + 1) + "—<i class=\"fa fa-linux\"></i>—" + ele.host_to_remote_user__host__name + "@" + ele.host_to_remote_user__host__ip_addr + "</h3> </div><div class=\"panel-body\"> <pre log_id='" + ele.id + "'>Start</pre> </div> </div>";
                $("#show_host_results").append(li_ele);
            });
            // Get Shell result//
            ResultRefresh = setInterval(function () {
                GetTaskResult(callbackdata.task_id);
            }, 2000);


        });
    }
    $("#recent_command_table").bootstrapTable('refresh', {});
}

//上傳文件路徑樣例
function show_file_demo() {
    $("#cmd_pannel").text("")
    $.niftyNoty({
        type: 'mint',
        // icon: 'fa fa-bolt fa-2x',
        // force: true,
        container: '#cmd_pannel',
        title:'【remote Path demo】 : /home/test2.jpg',
        message:'【  local path demo】 : C:\\Users\\BOSS\\Pictures\\2.jpg',
        closeBtn: true,
        timer: 10000
    });
}

//处理最近命令返回的结果
function show_cmd_with_result(cmdid,task) {
    $("#recent_command_pannel_alert").text("");
    $("#show_rencent_cmd_result_panel").removeClass("hidden")
    console.log("CMDID:" + cmdid);
    var csrftoken = $("input[name='csrfmiddlewaretoken']").val();
    $.getJSON('/recent_cmd_result_button/', {
        'cmdid': cmdid,
        'csrfmiddlewaretoken': csrftoken
    }, function (callback) {
        console.log("callback：" + callback)
        // var callbackdata = JSON.parse(callback);  已经 object对象，不需要在JSON.parse
        $.each(callback, function (index, ele) {
            if (ele.taskstatus == "Error") {
                recent_alert_type = 'danger'
                recent_alert_icon = 'fa fa-bolt fa-2x'
                status_lable_class = 'danger'
            } else if (ele.taskstatus == "Success") {
                recent_alert_type = 'success'
                recent_alert_icon = 'fa fa-flag fa-2x'
                status_lable_class = 'success'
            } else {
                recent_alert_type = 'warning'
                recent_alert_icon = 'fa fa-bell fa-2x'
                status_lable_class = 'warning'
            }
            $.niftyNoty({
                type: recent_alert_type,
                icon: 'fa fa-bolt fa-2x',
                // title:ele.taskstatus,
                // message:ele.taskresult,
                force: true,
                container: '#recent_command_pannel_alert',
                html: '<div class="panel panel-bordered panel-mint">\n' +
                    '<div class="panel-heading">\n' +
                    '<h3 class="panel-title"><span class="badge badge-purple">' + ele.taskid + '</span><span class="badge badge-warning">' + ele.username + '</span><span class="badge badge-mint">' + ele.cmdtype + '</span><span class="badge badge-info">' + ele.taskip + '：' + ele.taskport + '</span><span class="badge badge-pink">' + ele.taskdate + '</span><span class="label label-' + status_lable_class + ' pull-right">' + ele.taskstatus + '</span></h3>\n' +
                    '</div>\n' +
                    '<div class="panel-body">\n' +
                    '<span class="label label-mint" ><i class="btn-label fa fa-code"></i> ' + ele.command + '</span>\n' +
                    '<pre style="color: #1b1b1b;">' + ele.taskresult + '</pre>\n' +
                    '</div>\n' +
                    '</div>',
                closeBtn: true,
                // timer: 5000
            });

        })

    })


}

//处理host_record命令记录页面提交的Result结果按钮
function show_task_info_result(task_id,task) {
    console.log(task_id)
    console.log(task)
    $("#single_task_pannel_alert").text("");
    $("#show_single_task_info_pannel").removeClass("hidden");
    $.niftyNoty({
        type: 'primary',
        icon: 'fa fa-bolt fa-2x',
        // force: true,
        container: '#single_task_pannel_alert',
        html: '<pre style="color: #1b1b1b;max-height: 500px;">' + task.result + '</pre>',
        closeBtn: true,
        // timer: 5000
    });


// JavaScript onclick传递对象参数（easyui传递一行数据时）错误：uncaught SyntaxError: Unexpected identifier
//     用onclick传递对象参数时（easyui传递一行数据时），会报Sncaught SyntaxError: Unexpected identifier错误。
//     经查，onclick（对象）这种传递对象形式里面的对象会变成onclick（[object Object]）。
//     解决方法：将对象转化为json字符串，再将json字符串的双引号转换成单引号就行了
//     思路： JSON.stringify().replace(/\”/g,”’”)将对象转化成JSON字符串传递，函数接收后会自动变成对象（原理暂不清楚）。
//     过程解释： JSON.stringify()将对象转化成JSON字符串；.replace(/\”/g,”’”)将JSON字符串中的双引号转化成单引号，不然会报Unexpected end of input错误（这个错误是由于带的json字符串。它的双引号与onclick控件的双引号冲突了）
//
// 代码内容如下:传递参数
//     var $row = JSON.stringify(row).replace(/\"/g,"'");//row的是一个对象
//     <a href="#" onclick="editParentRow('+$row+')">编辑</a>//拼接传递对象





}

//处理提交的file命令
function run_shell_file(self) {
    $("#show_host_results").text("")           //重新点击按钮后，清空之前的运行结果
    var select_host_ids = [];
    var file_trans_type = $("#file_trans_type").val()
    var service_path = $("#service_path").val();
    var local_path = $("#local_path").val();
    $("[tag='host_select']:checked").each(
        function () {
            select_host_ids.push($(this).val())   //把所有选中的结果添加到列表中
        }
    )
    if (select_host_ids.length == 0) {
        $.niftyNoty({
            type: 'pink',
            container: '#select_host_pannel',
            html: '<div class="media">🙁Please select a host and try again！</div>',
            closeBtn: true,
            timer: 2000
        });
        // }else if(service_path.length<=1 || local_path.length<=1){
    } else if (service_path.length <= 1) {
        $.niftyNoty({
            type: 'pink',
            container: '#cmd_pannel',
            html: '<div class="media">请输入文件路径</div>',
            closeBtn: true,
            timer: 2000
        });

    } else {
        $(self).attr("disabled", "true");  //程序运行过程中禁止提交执行按钮
        $("#show_cmd_result").attr("class", " panel panel-bordered-primary ");    //显示运行结果框
        var csrftoken = $("input[name='csrfmiddlewaretoken']").val()    //获取CSRF TOKEN
        console.log("service_path:" + service_path);
        console.log("local_path:" + local_path);
        console.log("file_trans_type:" + file_trans_type);
        console.log("csrftoken:" + csrftoken);
        task_data = {
            "select_host_list": select_host_ids,
            "task_type": "file",
            "service_path": service_path,
            "local_path": local_path,
            "file_trans_type": file_trans_type,

        };
        $.post("/muilt_file_trans/", {
            "task_data": JSON.stringify(task_data),
            "csrfmiddlewaretoken": csrftoken
        }, function (callback) {
            console.log("task_callback:" + callback)
            var callbackdata = JSON.parse(callback);
            $.each(callbackdata.select_host_list, function (index, ele) {
                var li_ele = "<div pannelbox_id='" + ele.id + "' class=\"panel panel-bordered panel-dark \"><div class=\"panel-heading\"> <div class=\"panel-control\"> <div progressmain_id='" + ele.id + "' class=\"progress progress-md\" > <div progress_id='" + ele.id + "' style=\"width: 25%\" class=\"progress-bar progress-bar-primary progress-bar-striped active\"></div></div><button statusbutton_id='" + ele.id + "' class=\"btn btn-primary btn-labeled\" ><i statusi_id='" + ele.id + "' class=\"btn-label fa fa-gears\"  style=\" padding-left: 10px; border-left-width: 10px; \"></i> <span statusspan_id='" + ele.id + "'>Running</span></button></div><h3 class=\"panel-title\">" + (index + 1) + "—<i class=\"fa fa-linux\"></i>—" + ele.host_to_remote_user__host__name + "@" + ele.host_to_remote_user__host__ip_addr + "</h3> </div><div class=\"panel-body\"> <pre log_id='" + ele.id + "'>Start</pre> </div> </div>";
                $("#show_host_results").append(li_ele);
            });
            // Get Shell result//
            ResultRefresh = setInterval(function () {
                GetTaskResult(callbackdata.task_id);
            }, 2000);
        });

    }


}

//处理批量命令返回的结果
function GetTaskResult(task_id) {
    $.getJSON("/get_task_result/", {"task_id": task_id}, function (callback) {
        console.log("data_callback:" + callback)
        var all_finish = true;
        $.each(callback, function (index, ele) {
            var pre_ele = $("pre[log_id=" + ele.id + "]")
            pre_ele.text(ele.result)
            if (ele.status == 0) {
                all_finish = false
            }
            if (pre_ele.text() == 'Init') {
                $("div[progress_id=" + ele.id + "]").css({width: "50%"})
                $("div[pannelbox_id=" + ele.id + "]").attr("class", " panel panel-bordered panel-mint ");
            }
            if (ele.status == 2) {
                $("div[progressmain_id=" + ele.id + "]").css({display: "none"})
                $("div[pannelbox_id=" + ele.id + "]").attr("class", " panel panel-bordered panel-danger ");
                $("i[statusi_id=" + ele.id + "]").attr("class", " btn-label fa fa-window-close-o ");
                $("span[statusspan_id=" + ele.id + "]").text("Error!!!!!!");
            }
            if (ele.status == 3) {
                $("div[progressmain_id=" + ele.id + "]").css({display: "none"})
                $("div[pannelbox_id=" + ele.id + "]").attr("class", " panel panel-bordered panel-success ");
                $("i[statusi_id=" + ele.id + "]").attr("class", " btn-label fa fa-hand-peace-o ");
                $("span[statusspan_id=" + ele.id + "]").text("Success");
            }
        })

        console.log(all_finish)
        if (all_finish) {
            clearInterval(ResultRefresh) //停止运行方法
            $("#run_cmd_button").attr("disabled", false); //任务结束，恢复执行按钮
            $("#run_file_button").attr("disabled", false); //任务结束，恢复执行按钮
            console.log("All command are finish!")
        }
    })
}

function select_host_checkbox(self) {
    console.log("select_host_checkbox成功运行")
    if (self.checked) {
        console.log(self.checked)
        $("input[name='selectitem']").each(function (i, n) {
            n.checked = true;
        });
    } else {
        console.log(self.checked)
        $("input[name='selectitem']").each(function (i, n) {
            n.checked = false;
        });
    }
    select_host_cmd()
}

function select_host_cmd(self) {
    console.log("select_host_cmd 成功运行")
    var select_host_ids = []
    $("[tag=host_select]:checked").each(function () {
        select_host_ids.push($(this).val())
    })
    console.log(select_host_ids)
    var csrftoken = $("input[name='csrfmiddlewaretoken']").val()
    $.post("/host_select_record/", {
        'select_host_ids': JSON.stringify(select_host_ids),
        'csrfmiddlewaretoken': csrftoken
    }, function () {
    })
    $("#sk_wave_spinkit").removeClass("hidden")
    var x = (1 + Math.ceil(Math.random() * 5)) * 1000;
    console.log('x=' + x)
    setTimeout('refresh_table()', x)  //设置延时执行方法
    setTimeout('sk_wave_spinkit_control()', x)  //设置延时执行方法


}

//调用bootstrapTable的表格刷新方法
function refresh_table() {
    $("#host_record_result_table").bootstrapTable('refresh', {});
}

//加载数据期间运行加载波浪sk_wave_spinkit友好动画
function sk_wave_spinkit_control() {
    $("#sk_wave_spinkit").addClass("hidden")
}

//处理左侧菜单选中的状态
function active_menu() {
    var menupath = window.location.pathname
    // console.log(window.location.href)     //   取浏览器全地址  //  http://127.0.0.1:8000/host_muilt/?sss=1
    // console.log(menupath)    //    取浏览器地址后的路径  //  /host_muilt/
    // class="collapse in"
    // $("a[href='/web_ssh/']").attr("class", "active-link");   //成功
    // $("#mainnav-menu li").find("a[href='/web_ssh/']").parent().attr("class", "active-link");  //成功
    // $("#mainnav-menu li").find("a").attr("href",menupath).parent().addClass("active-link");
    $("#mainnav-menu li").find("a[href='" + menupath + "']").parent().addClass("active-link");
    $("#mainnav-menu-sub li").find("a[href='" + menupath + "']").parent().addClass("active-link");
    $("#mainnav-menu-sub li").find("a[href='" + menupath + "']").parent().parent().addClass("collapse in");
}

//程序运行完以后激活tooltips,popover工具
//bootstrap tooltips,popover 在表格中无法使用，需要在程序运行结尾激活，一下是激活代码
$(document).ready(function () {
    $("body").tooltip({selector: '[data-toggle=tooltip]'});
    $("body").popover({selector: '[data-toggle=popover]'});
});
