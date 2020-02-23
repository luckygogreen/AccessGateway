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
                        success: function (callback) {
                            callback = JSON.parse(callback)
                            if (callback == "success") {
                                $.niftyNoty({
                                    type: 'success',
                                    icon: 'pli-like-2 icon-2x',
                                    message: 'The task has beed changed successfully! ',
                                    container: 'floating',
                                    timer: 5000
                                });
                                $('#user_idc').append('<option selected>' + $('#add_new_idc_tag').val() + '</option>');
                                $('#user_idc').selectpicker('refresh');
                            } else if (callback == 'name_used') {
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
                        success: function (callback) {
                            callback = JSON.parse(callback)
                            if (callback == "success") {
                                $.niftyNoty({
                                    type: 'success',
                                    icon: 'pli-like-2 icon-2x',
                                    message: 'The task has beed changed successfully! ',
                                    container: 'floating',
                                    timer: 5000
                                });
                                $('#user_groups').append('<option selected>' + $('#add_new_group_tag').val() + '</option>');
                                $('#user_groups').selectpicker('refresh');
                            } else if (callback == 'name_used') {
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
    var newip = $("#new_ipaddress").val();
    var newport = $("#new_port").val();
    var newusername = $("#new_remote_username").val();
    var newpassword = $("#new_remote_password").val();
    var newidc = $("#user_idc").val();
    var newgroup = $("#user_groups").val();
    // console.log(newip);
    // console.log(newport);
    // console.log(newusername);
    // console.log(newpassword);
    // console.log(newidc);
    // console.log(newgroup);
    var data_dict = {
        'newip': newip,
        'newport': newport,
        'newusername': newusername,
        'newpassword': newpassword,
        'newidc': newidc,
        'newgroup': newgroup
    }
    $.post('/user_and_new_host/', {'data': JSON.stringify(data_dict),'csrfmiddlewaretoken': $("input[name='csrfmiddlewaretoken']").val()}, function (callback) {
        callback = JSON.parse(callback)
        if (callback == "success") {
            $.niftyNoty({
                type: 'success',
                icon: 'pli-like-2 icon-2x',
                message: 'The task has beed changed successfully! ',
                container: 'floating',
                timer: 5000
            });
            $('#user_groups').append('<option selected>' + $('#add_new_group_tag').val() + '</option>');
            $('#user_groups').selectpicker('refresh');
        } else if (callback == 'name_used') {
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
    })
}