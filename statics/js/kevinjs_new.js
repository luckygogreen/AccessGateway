//get all select host id
function get_all_select_host_id() {
    console.log('get_all_select_host_id running');
    var host_select_list = [];
    $("[tag='host_select']:checked").each(
        function () {
            host_select_list.push($(this).val());
        }
    );
    return host_select_list;
}

//post post_periodic_task to view
function post_periodic_task_button(data_dict, csrfmiddlewaretoken) {
    console.log('post_periodic_task_button running');
    $.post('/periodic_task_post_views/', {
        'csrfmiddlewaretoken': csrfmiddlewaretoken,
        'data_dict': JSON.stringify(data_dict)
    }, function (callback) {
        console.log(callback);
    });

}

function if_required_fields(shedule_type) {
    console.log('if_required_fields running');
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


function corntab_periodic_task_button(host_select_list) {
    console.log('corntab_periodic_task_button running');
    // get CSRF TOKEN
    var csrftoken = $("input[name='csrfmiddlewaretoken']").val();
    // get all corntab task data
    var periodic_task_sechdule_type = 'Corntab';
    var periodic_task_name = $("#periodic_task_name").val();
    var periodic_task_command = $("#periodic_task_command").val();
    var periodic_task_ime_zone = $("#demo-chosen-select").val();
    var corntab_month_val = $("#corntab_month_val").text();
    var corntab_day_val = $("#corntab_day_val").text();
    var corntab_weekday_val = $("#corntab_weekday_val").text();
    var corntab_hour_val = $("#corntab_hour_val").text();
    var corntab_minute_val = $("#corntab_minute_val").text();
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
    // data_dict = JSON.stringify(data)
    //post dict to AJAX POST function
    post_periodic_task_button(data_dict, csrftoken);

}





