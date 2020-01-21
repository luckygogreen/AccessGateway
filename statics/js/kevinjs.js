// 全选反选  单组复选框
function checkall(selectStatus) {
    //传入参数（全选框的选中状态）
    //根据name属性获取到单选框的input，使用each方法循环设置所有单选框的选中状态
    if (selectStatus) {
        $("input[name='selectitem']").each(function (i, n) {
            n.checked = true;
        });
    } else {
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

//  用来处理提交的CMD命令
function run_shell_cmd() {
    var cmd_text = $("#cmdtext").val();      //获取指定id的 value 值
    var select_host_ids = [];
    $("[tag='host_select']:checked").each(
        function () {
            select_host_ids.push($(this).val())
        }
    )
    // console.log(select_host_ids)
    // console.log(cmd_text)
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
        var csrftoken = $("input[name='csrfmiddlewaretoken']").val()
        $.post("/batch_task_mgr/", {'task_data':JSON.stringify(task_mgr),'csrfmiddlewaretoken':csrftoken}, function (callback) {
            console.log("task_callback:", task_mgr)
        });  //end post
    }
}