//get all select host id
function get_all_select_host_id() {
    var host_select_list = [];
    $("[tag='host_select']:checked").each(
        function () {
            host_select_list.push($(this).val());
        }
    );
    return host_select_list;
}

//if required fields = empty
function if_required_fields(shedule_type) {
    host_select_list = get_all_select_host_id();
    if (host_select_list.length <= 0) {
        $.niftyNoty({
            type: 'danger',
            icon: 'pli-cross icon-2x',
            message: 'Please select a server to operate',
            container: 'floating',
            timer: 5000
        });
    } else if ($('#periodic_task_name').val().length <= 0) {
        $.niftyNoty({
            type: 'danger',
            icon: 'pli-cross icon-2x',
            message: 'Please give the task a name',
            container: 'floating',
            timer: 5000
        });
    } else if ($('#periodic_task_command').val().length <= 0) {
        $.niftyNoty({
            type: 'danger',
            icon: 'pli-cross icon-2x',
            message: 'Please enter a command to execute',
            container: 'floating',
            timer: 5000
        });
    } else {
        if (shedule_type == 'corntab') {
            corntab_periodic_task_button(host_select_list);
        } else if (shedule_type == 'interval') {
            //for future imporve
        } else if (shedule_type == 'clocked') {
            //for future imporve
        } else {
            //for future imporve
        }

    }
}

// get all data
function corntab_periodic_task_button(host_select_list) {
    // get CSRF TOKEN
    var csrftoken = $("input[name='csrfmiddlewaretoken']").val();
    // get all corntab task data
    var periodic_task_sechdule_type = 'Corntab';
    var periodic_task_name = $("#periodic_task_name").val();
    var periodic_task_command = $("#periodic_task_command").val();
    var periodic_task_ime_zone = $("#demo-chosen-select").val();
    if ($("#corntab_month_val").text() == '0') {
        var corntab_month_val = '*'
    } else {
        var corntab_month_val = $("#corntab_month_val").text();
    }
    if ($("#corntab_day_val").text() == '0') {
        var corntab_day_val = '*'
    } else {
        var corntab_day_val = $("#corntab_day_val").text();
    }
    if ($("#corntab_weekday_val").text() == '0') {
        var corntab_weekday_val = '*'
    } else {
        var corntab_weekday_val = $("#corntab_weekday_val").text();
    }
    if ($("#corntab_hour_val").text() == '0') {
        var corntab_hour_val = '*'
    } else {
        var corntab_hour_val = $("#corntab_hour_val").text();
    }
    if ($("#corntab_minute_val").text() == '0') {
        var corntab_minute_val = '*'
    } else {
        var corntab_minute_val = $("#corntab_minute_val").text();
    }
    var select_host = host_select_list;
    // //check all value had been gotten
    // console.log(periodic_task_sechdule_type);
    // console.log(periodic_task_name);
    // console.log(periodic_task_command);
    // console.log(periodic_task_ime_zone);
    // console.log(corntab_month_val);
    // console.log(corntab_day_val);
    // console.log(corntab_weekday_val);
    // console.log(corntab_hour_val);
    // console.log(corntab_minute_val);
    // console.log(select_host);
    //create data_dictionary
    var data_dict = {
        'periodic_task_sechdule_type': periodic_task_sechdule_type,
        'periodic_task_name': periodic_task_name,
        'periodic_task_command': periodic_task_command,
        'periodic_task_timezone': periodic_task_ime_zone,
        'corntab_month_val': corntab_month_val,
        'corntab_day_val': corntab_day_val,
        'corntab_weekday_val': corntab_weekday_val,
        'corntab_hour_val': corntab_hour_val,
        'corntab_minute_val': corntab_minute_val,
        'select_host': select_host
    }
    post_periodic_task_button(data_dict, csrftoken);

}

//post post_periodic_task to view
function post_periodic_task_button(data_dict, csrfmiddlewaretoken) {
    $.post('/periodic_task_post_views/', {
        'csrfmiddlewaretoken': csrfmiddlewaretoken,
        'data_dict': JSON.stringify(data_dict)
    }, function (callback) {
        callback = JSON.parse(callback)
        if (callback == 'taskname_used') {
            $.niftyNoty({
                type: 'danger',
                icon: 'pli-cross icon-2x',
                message: 'The task name was alraedy been taken!',
                container: 'floating',
                timer: 5000
            });
        } else if (callback == 'servererror') {
            $.niftyNoty({
                type: 'danger',
                icon: 'pli-cross icon-2x',
                message: 'Service busy please try again ',
                container: 'floating',
                timer: 5000
            });
        } else if (callback == 'success') {
            $.niftyNoty({
                type: 'success',
                icon: 'pli-like-2 icon-2x',
                message: 'The task has beed created successfully! ',
                container: 'floating',
                timer: 5000
            });
            $("#periodic_history_table_crontab").bootstrapTable('refresh',setTimeout(1000));
        } else {
            $.niftyNoty({
                type: 'danger',
                icon: 'pli-cross icon-2x',
                message: 'Unknow error please contact amdin ',
                container: 'floating',
                timer: 5000
            });
        }
    });

}


//AJAX page refresh or data refresh
function periodic_history_table_refresh() {
    // console.log('okookokokokooko')
    $("#periodic_history_table_crontab").bootstrapTable('destroy'); // 销毁数据表格
    $("#periodic_history_table_crontab").bootstrapTable('refresh',setTimeout(1000)); //刷新最新数据表格
}


//All sechdule type history delete button
function all_task_delete_button(del_id) {
    bootbox.confirm("<h3>Are you sure?</h3><br><h5>Once deleted, tasks cannot be recovered,are you ok with that ?</h5>", function (result) {
        var csrftoken = $("input[name='csrfmiddlewaretoken']").val();
        if (result) {
            $.post("/all_task_delete_button/", {
                'seleteid': JSON.stringify(del_id),
                'csrfmiddlewaretoken': csrftoken
            }, function (callback) {
                callback = JSON.parse(callback)
                if (callback == "deleteSuccess") {
                    $.niftyNoty({
                        type: 'success',
                        icon: 'pli-like-2 icon-2x',
                        message: 'The task has beed delete successfully! ',
                        container: 'floating',
                        timer: 5000
                    });
                    $("#periodic_history_table_crontab").bootstrapTable('refresh',setTimeout(1000));
                    // $("#periodic_history_table_crontab").bootstrapTable('refresh'); //刷新最新数据表格
                } else {
                    $.niftyNoty({
                        type: 'danger',
                        icon: 'pli-cross icon-2x',
                        message: callback,
                        container: 'floating',
                        timer: 5000
                    });
                }
            });
        } else {
            // console.log("nothing to do !")
        }
        ;

    });
}

//all sechdule type history change status button
function change_task_status_button(taskid, taskstatus) {
    var csrftoken = $("input[name='csrfmiddlewaretoken']").val();
    $.post('/all_task_edit_button/', {
        'csrfmiddlewaretoken': csrftoken,
        'taskid': JSON.stringify(taskid),
        'taskstatus': JSON.stringify(taskstatus)
    }, function (callback) {
        callback = JSON.parse(callback)
        if (callback == 'statuschangeTure') {
            $.niftyNoty({
                type: 'success',
                icon: 'pli-like-2 icon-2x',
                message: 'The task is run now! ',
                container: 'floating',
                timer: 5000
            });
            $("#periodic_history_table_crontab").bootstrapTable('refresh',setTimeout(1000));
        } else if (callback == 'statuschangeFalse') {
            $.niftyNoty({
                type: 'success',
                icon: 'pli-like-2 icon-2x',
                message: 'The task is stop now! ',
                container: 'floating',
                timer: 5000
            });
            $("#periodic_history_table_crontab").bootstrapTable('refresh',setTimeout(1000));
        } else {
            $.niftyNoty({
                type: 'danger',
                icon: 'pli-cross icon-2x',
                message: 'Server busy ,please try again!',
                container: 'floating',
                timer: 5000
            });
        }

    });
}






