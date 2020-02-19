// Form-Component.js
// ====================================================================
// This file should not be included in your project.
// This is just a sample how to initialize plugins or components.
$(document).on('nifty.ready', function () {
    //default date
    var mydate = new Date();
    var month = mydate.getMonth() + 1;
    var day = mydate.getDate();
    month = (month.toString().length == 1) ? ("0" + month) : month;
    day = (day.toString().length == 1) ? ("0" + day) : day;
    var result = month + '/' + day + '/' + mydate.getFullYear(); //当前日期
    $('#onetime_datapicker').val(result);
    // CHOSEN TIME ZONE
    $('#demo-chosen-select').chosen();
    // BOOTSTRAP DATEPICKER WITH AUTO CLOSE
    $('#demo-dp-component .input-group.date').datepicker({
        autoclose: true,
        todayHighlight: true,
        todayBtn: "linked",
    });
    // BOOTSTRAP TIMEPICKER
    $('#demo-tp-com').timepicker();




});

