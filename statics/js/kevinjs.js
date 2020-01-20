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