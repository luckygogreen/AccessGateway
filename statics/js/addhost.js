// BOOTBOX - CUSTOM HTML FORM
// =================================================================
// Require Bootbox
// http://bootboxjs.com/
// =================================================================
//ADD IDC
$('#add_idc_tag').on('click', function () {
    bootbox.dialog({
        title: "Add IDC",
        message: '<div class="form-group">\n' +
            '\t\t\t\t\t                        <label for="add_new_idc_tag" class="col-sm-3 control-label">IDC Name</label>\n' +
            '\t\t\t\t\t                        <div class="col-sm-6">\n' +
            '\t\t\t\t\t                            <input type="text" placeholder="IDC Name" class="form-control input-lg" id="add_new_idc_tag">\n' +
            '\t\t\t\t\t                        </div>\n' +
            '\t\t\t\t\t                    </div>',
        buttons: {
            success: {
                label: "Save",
                className: "btn-success",
                callback: function () {
                    $.ajax({
                        type: 'post',
                        url: '/add_idc_tag_to_user/',
                        data: {
                            'data': JSON.stringify($('#add_new_idc_tag').val()),
                            'csrfmiddlewaretoken': $("input[name='csrfmiddlewaretoken']").val()
                        },
                        dataType: 'json',
                        cache: false,
                        success: function (callback1) {
                            // callback1 = JSON.parse(callback1);
                            // console.log(callback1);
                            if (callback1 == "success") {
                                $.niftyNoty({
                                    type: 'success',
                                    icon: 'pli-like-2 icon-2x',
                                    message: 'The IDC beed created successfully! ',
                                    container: 'floating',
                                    timer: 5000
                                });
                                $('#user_idc').append('<option selected>' + $('#add_new_idc_tag').val() + '</option>');
                                $('#user_idc').selectpicker('refresh');
                            } else if (callback1 == 'name_used') {
                                $.niftyNoty({
                                    type: 'danger',
                                    icon: 'pli-cross icon-2x',
                                    message: 'The IDC name is already been taken',
                                    container: 'floating',
                                    timer: 5000
                                });
                            } else {
                                $.niftyNoty({
                                    type: 'danger',
                                    icon: 'pli-cross icon-2x',
                                    message: 'Server busy,please try again later',
                                    container: 'floating',
                                    timer: 5000
                                });
                            }
                        },
                        error: function () {
                            $.niftyNoty({
                                type: 'danger',
                                icon: 'pli-cross icon-2x',
                                message: 'Unknow error please contact admin ',
                                container: 'floating',
                                timer: 5000
                            });
                        },
                    });
                }
            }
        }
    });
});

//ADD Group
$('#add_group_tag').on('click', function () {
    bootbox.dialog({
        title: "Add Group",
        message: '<div class="form-group">\n' +
            '\t\t\t\t\t                        <label for="add_new_group_tag" class="col-sm-3 control-label">Group Name</label>\n' +
            '\t\t\t\t\t                        <div class="col-sm-6">\n' +
            '\t\t\t\t\t                            <input type="text" placeholder="Group Name" class="form-control input-lg" id="add_new_group_tag">\n' +
            '\t\t\t\t\t                        </div>\n' +
            '\t\t\t\t\t                    </div>',
        buttons: {
            success: {
                label: "Save",
                className: "btn-success",
                callback: function () {
                    $.ajax({
                        type: 'post',
                        url: '/add_group_tag_to_user/',
                        data: {
                            'data': JSON.stringify($('#add_new_group_tag').val()),
                            'csrfmiddlewaretoken': $("input[name='csrfmiddlewaretoken']").val()
                        },
                        dataType: 'json',
                        cache: false,
                        success: function (callback1) {
                            // callback1 = JSON.parse(callback1);
                            // console.log(callback1);
                            if (callback1 == "success") {
                                $.niftyNoty({
                                    type: 'success',
                                    icon: 'pli-like-2 icon-2x',
                                    message: 'The Group has beed created successfully! ',
                                    container: 'floating',
                                    timer: 5000
                                });
                                $('#user_groups').append('<option selected>' + $('#add_new_group_tag').val() + '</option>');
                                $('#user_groups').selectpicker('refresh');
                            } else if (callback1 == 'name_used') {
                                $.niftyNoty({
                                    type: 'danger',
                                    icon: 'pli-cross icon-2x',
                                    message: 'The IDC name is already been taken',
                                    container: 'floating',
                                    timer: 5000
                                });
                            } else {
                                $.niftyNoty({
                                    type: 'danger',
                                    icon: 'pli-cross icon-2x',
                                    message: 'Server busy,please try again later',
                                    container: 'floating',
                                    timer: 5000
                                });
                            }
                        },
                        error: function () {
                            $.niftyNoty({
                                type: 'danger',
                                icon: 'pli-cross icon-2x',
                                message: 'Unknow error please contact admin ',
                                container: 'floating',
                                timer: 5000
                            });
                        },
                    });
                }
            }
        }
    });
});


//Add new host
function user_add_new_host_button() {
    var newhostname = $("#new_hostname").val();
    var newip = $("#new_ipaddress").val();
    var newport = $("#new_port").val();
    var newusername = $("#new_remote_username").val();
    var newpassword = $("#new_remote_password").val();
    var newpasstype = '0'
    var newidc = $("#user_idc").val();
    var newgroup = $("#user_groups").val();
    var ip_ok = checkIP(newip);
    // console.log(newhostname);
    // console.log(newip);
    // console.log(newport);
    // console.log(newusername);
    // console.log(newpassword);
    // console.log(newpasstype);
    // console.log(newidc);
    // console.log(newgroup);
    if (newhostname.length <= 1) {
        $.niftyNoty({
            type: 'danger',
            icon: 'pli-cross icon-2x',
            message: 'Please enter a server name',
            container: 'floating',
            timer: 5000
        });
    } else if (ip_ok == false) {
        $.niftyNoty({
            type: 'danger',
            icon: 'pli-cross icon-2x',
            message: 'Please enter a effective IP address',
            container: 'floating',
            timer: 5000
        });
    } else if (newport.length <= 0) {
        $.niftyNoty({
            type: 'danger',
            icon: 'pli-cross icon-2x',
            message: 'Please enter a Port',
            container: 'floating',
            timer: 5000
        });
    } else if (newusername.length <= 0) {
        $.niftyNoty({
            type: 'danger',
            icon: 'pli-cross icon-2x',
            message: 'Please enter a Login name',
            container: 'floating',
            timer: 5000
        });
    } else {
        var data_dict = {
            'newhostname': newhostname,
            'newip': newip,
            'newport': newport,
            'newusername': newusername,
            'newpassword': newpassword,
            'pass_tyoe': newpasstype,
            'newidc': newidc,
            'newgroup': newgroup
        }
        $.post('/user_and_new_host/', {
            'data': JSON.stringify(data_dict),
            'csrfmiddlewaretoken': $("input[name='csrfmiddlewaretoken']").val()
        }, function (callback) {
            callback = JSON.parse(callback);
            if (callback == "singlesuccess") {
                $.niftyNoty({
                    type: 'success',
                    icon: 'pli-like-2 icon-2x',
                    message: 'The host has beed created successfully! ',
                    container: 'floating',
                    timer: 5000
                });
            } else if (callback == "groupsuccess") {
                $.niftyNoty({
                    type: 'success',
                    icon: 'pli-like-2 icon-2x',
                    message: 'The host has beed created successfully! ',
                    container: 'floating',
                    timer: 5000
                });
                window.location.reload();
                $("#"+newgroup+"").attr('class','collapse in');
            }else if (callback == 'nameused') {
                $.niftyNoty({
                    type: 'danger',
                    icon: 'pli-cross icon-2x',
                    message: 'The IDC name is already been taken',
                    container: 'floating',
                    timer: 5000
                });
            } else if (callback == 'hostused') {
                $.niftyNoty({
                    type: 'warning',
                    icon: 'pli-cross icon-2x',
                    message: 'Server IP already exists',
                    container: 'floating',
                    timer: 5000
                });
            } else if (callback == 'hostname_used'){
                $.niftyNoty({
                    type: 'warning',
                    icon: 'pli-cross icon-2x',
                    message: 'Server Name already exists',
                    container: 'floating',
                    timer: 5000
                });
            } else {
                $.niftyNoty({
                    type: 'danger',
                    icon: 'pli-cross icon-2x',
                    message: 'Server busy,please try again later',
                    container: 'floating',
                    timer: 5000
                });
            }
        })

    }


}


//判断ip地址的合法性
function checkIP(value) {
    var exp = /^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$/;
    var reg = value.match(exp);
    if (reg == null) {
        return false;
    }else {
        return true;
    }
}