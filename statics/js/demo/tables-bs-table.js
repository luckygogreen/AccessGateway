// Tables-BS-Table.js
// ====================================================================
// This file should not be included in your project.
// This is just a sample how to initialize plugins or components.
//
// - ThemeOn.net -


$(document).on('nifty.ready', function () {


    // BOOTSTRAP TABLES USING FONT AWESOME ICONS
    // =================================================================
    // Require Bootstrap Table
    // http://bootstrap-table.wenzhixin.net.cn/
    //
    // =================================================================
    jQuery.fn.bootstrapTable.defaults.icons = {
        paginationSwitchDown: 'demo-pli-arrow-down',
        paginationSwitchUp: 'demo-pli-arrow-up',
        refresh: 'demo-pli-repeat-2',
        toggle: 'demo-pli-layout-grid',
        columns: 'demo-pli-check',
        detailOpen: 'demo-psi-add',
        detailClose: 'demo-psi-remove'
    }


    // EDITABLE - COMBINATION WITH X-EDITABLE
    // =================================================================
    // Require X-editable
    // http://vitalets.github.io/x-editable/
    //
    // Require Bootstrap Table
    // http://bootstrap-table.wenzhixin.net.cn/
    //
    // Require X-editable Extension of Bootstrap Table
    // http://bootstrap-table.wenzhixin.net.cn/
    // =================================================================
    $.fn.editable.defaults.ajaxOptions = {type: "post"}
    $('#periodic_history_table_crontab').bootstrapTable({
        idField: 'task_id',
        onEditableSave: function (field, row, oldValue, $el) {//编辑单元格事件
            $.ajax({
                type: 'post',
                url: '/perioidc_task_name_edit/',
                data: {
                    'data': JSON.stringify(row),
                    'csrfmiddlewaretoken': $("input[name='csrfmiddlewaretoken']").val()
                },    //var csrftoken = $("input[name='csrfmiddlewaretoken']").val();
                dataType: 'json',
                cache: false,
                success: function (data) {
                    if ("success" == data) {
                        $.niftyNoty({
                            type: 'success',
                            icon: 'pli-like-2 icon-2x',
                            message: 'The task has beed changed successfully! ',
                            container: 'floating',
                            timer: 5000
                        });
                        $("#periodic_history_table_crontab").bootstrapTable('refresh',setTimeout(1000)); //刷新最新数据表格
                    } else if (data == 'name_used') {
                        $.niftyNoty({
                            type: 'danger',
                            icon: 'pli-cross icon-2x',
                            message: 'The task name is already been taken',
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
                        message: 'Unknow error please contact amdin ',
                        container: 'floating',
                        timer: 5000
                    });
                },
            });
        },
        columns: [{
            field: 'task_id',
            formatter: 'invoiceFormatter',
            align: 'center',
            title: 'ID'
        }, {
            field: 'task_name',
            title: 'Task Name',
            align: 'center',
            orderable: true,
            editable: {
                type: 'text',
                validate: function (value) {
                    if ($.trim(value) == "") return "This field is required";
                }
            }
        }, {
            field: 'task_sechdule',
            formatter: 'dateFormatter',
            align: 'center',
            title: 'Sechdule',
        }, {
            field: 'task_status',
            formatter: 'periodicTaskStatusFormatter',
            align: 'center',
            title: 'Status',
        }, {
            field: 'task_id',
            formatter: 'taskdeletebuttonFormatter',
            align: 'center',
            title: 'Operating',
        }]
    });


    // X-EDITABLE USING FONT AWESOME ICONS
    // =================================================================
    // Require X-editable
    // http://vitalets.github.io/x-editable/
    //
    // Require Font Awesome
    // http://fortawesome.github.io/Font-Awesome/icons/
    // =================================================================
    // $.fn.editableform.buttons =
    //     '<button type="submit" class="btn btn-primary editable-submit">' +
    //     '<i class="fa fa-fw fa-check"></i>' +
    //     '</button>' +
    //     '<button type="button" class="btn btn-default editable-cancel">' +
    //     '<i class="fa fa-fw fa-times"></i>' +
    //     '</button>';


    // BOOTSTRAP TABLE - CUSTOM TOOLBAR
    // =================================================================
    // Require Bootstrap Table
    // http://bootstrap-table.wenzhixin.net.cn/
    // =================================================================
    var $table = $('#demo-custom-toolbar'), $remove = $('#demo-delete-row');

    $table.on('check.bs.table uncheck.bs.table check-all.bs.table uncheck-all.bs.table', function () {
        $remove.prop('disabled', !$table.bootstrapTable('getSelections').length);
    });

    $remove.click(function () {
        var ids = $.map($table.bootstrapTable('getSelections'), function (row) {
            return row.id
        });
        $table.bootstrapTable('remove', {
            field: 'id',
            values: ids
        });
        $remove.prop('disabled', true);
    });


});


// FORMAT COLUMN
// Use "data-formatter" on HTML to format the display of bootstrap table column.
// =================================================================


// Sample format for Invoice Column.
// =================================================================
function invoiceFormatter(value, row) {
    return '<span >#' + value + '</span>';
}


//task_status Formatter
function intervalStatusFormatter(value, row) {
    console.log(row)
    ele = "";
    if (value == true) {
        ele = '<span class="label label-success">Run</span>';
    } else {
        ele = '<span class="label label-danger">Stop</span>';
    }
    return ele;
}

//all_periodic_task_status Formatter
function periodicTaskStatusFormatter(value, row) {
    ele = "";
    if (value == true) {
        ele = '<button id="taskstatus_' + row.task_id + '" statusidtag="' + row.task_id + '" class="btn btn-xs btn-success" onclick="change_task_status_button(' + row.task_id + ',' + row.task_status + ')">Run</button>';
    } else {
        ele = '<button id="taskstatus_' + row.task_id + '" statusidtag="' + row.task_id + '" class="btn btn-xs btn-danger" onclick="change_task_status_button(' + row.task_id + ',' + row.task_status + ')">Stop</button>';
    }
    return ele;
}


//all_periodic_task_status Formatter
function taskstatusFormatter(value, row) {
    ele = "";
    if (value == true) {
        ele = '<span class="label label-warning">Waiting</span>';
    } else {
        ele = '<span class="label label-success">complete</span>';
    }
    return ele;
}

function tasksoperatingFormatter(value, row) {
    ele = '<button class="btn btn-xs btn-danger btn-icon" id="task_delete_button' + value + '" value="' + value + '" onclick="one_time_task_delete_button(' + value + ')"><i class="demo-psi-recycling icon-lg"></i></button>';
    return ele;
}

function taskintervaldeleteFormatter(value, row) {
    ele = '<button class="btn btn-xs btn-danger btn-icon" id="task_delete_button' + value + '" value="' + value + '" onclick="interval_task_button(' + value + ')"><i class="demo-psi-recycling icon-lg"></i></button>';
    return ele;
}

function taskdeletebuttonFormatter(value, row) {
    ele = '<button class="btn btn-xs btn-danger btn-icon" id="task_delete_button' + value + '" value="' + value + '" onclick="all_task_delete_button(' + value + ')"><i class="demo-psi-recycling icon-lg"></i></button>';
    return ele;
}


function resultToplip(value, row) {
    var html_cmd_result = '<button class="btn btn-xs btn-default add-tooltip" data-html="true" data-toggle="tooltip" data-container="body" data-placement="top" data-original-title="' + value + '">Show</button>'
    return html_cmd_result
}

//host_muilt 批量命令页面结果result按钮样式
function click_small_button(value, row) {
    console.log(row)
    var html_cmd_result = '<button class="btn btn-primary btn-labeled btn-xs" onclick="show_cmd_with_result(' + value + ')"><i class="btn-label fa fa-code"></i> Show</button>'
    return html_cmd_result
}

//host_record 命令操作记录页面结果result按钮样式
function task_result_button(value, row) {
    var task = JSON.stringify(row).replace(/\"/g, "'");
    var html_cmd_result = '<button class="btn btn-primary btn-labeled btn-xs" onclick="show_task_info_result(' + value + ',' + task + ')"><i class="btn-label fa fa-code"></i> Show</button>'
    return html_cmd_result
}


// Sample Format for User Name Column.
// =================================================================
function nameFormatter(value, row) {
    return '<a href="#" class="btn-link" > ' + value + '</a>';
}


// Sample Format for Order Date Column.
// =================================================================
function dateFormatter(value, row) {
    var icon = row.id % 2 === 0 ? 'fa-star' : 'fa-user';
    return '<span class="text-muted"><i class="fa fa-clock-o"></i> ' + value + '</span>';
}


// Sample Format for Order Status Column.
// =================================================================
function statusFormatter(value, row) {
    var labelColor;
    if (value == "Success") {
        labelColor = "success";
    } else if (value == "Error") {
        labelColor = "danger";
    } else {
        labelColor = "warning";
    }
    var icon = row.id % 2 === 0 ? 'fa-star' : 'fa-user';
    return '<div class="label label-table label-' + labelColor + '"> ' + value + '</div>';
}


// Sample Format for Tracking Number Column.
// =================================================================
function trackFormatter(value, row) {
    if (value) return '<i class="fa fa-plane"></i> ' + value;
}


// Sort Price Column
// =================================================================
function priceSorter(a, b) {
    a = +a.substring(1); // remove $
    b = +b.substring(1);
    if (a > b) return 1;
    if (a < b) return -1;
    return 0;
}

