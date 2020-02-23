// Form-Component.js
// ====================================================================
// This file should not be included in your project.
// This is just a sample how to initialize plugins or components.
$(document).on('nifty.ready', function () {

    // CHOSEN TIME ZONE
    $('#demo-chosen-select').chosen();

    // DEFAULT RANGE SLIDER Day of month
    var corntab_day = document.getElementById('corntab_day');
    var corntab_day_val = document.getElementById('corntab_day_val');
    noUiSlider.create(corntab_day, {
        start: [0],
        connect: 'lower',
        range: {
            'min': [0],
            'max': [31]
        }
    });
    corntab_day.noUiSlider.on('update', function (values, handle) {
        corntab_day_val.innerHTML = values[handle].split('.')[0]; //.split('.')[0]  从点开始,全部去掉，0表示全部去掉，点表示从点开始
    });


    // DEFAULT RANGE SLIDER Month of year
    var corntab_month = document.getElementById('corntab_month');
    var corntab_month_val = document.getElementById('corntab_month_val');
    noUiSlider.create(corntab_month, {
        start: [0],
        connect: 'lower',
        range: {
            'min': [0],
            'max': [12]
        }
    });
    corntab_month.noUiSlider.on('update', function (values, handle) {
        corntab_month_val.innerHTML = values[handle].split('.')[0]; //.split('.')[0]  从点开始,全部去掉，0表示全部去掉，点表示从点开始
    });


    // DEFAULT RANGE SLIDER Day of Week
    var corntab_weekday = document.getElementById('corntab_weekday');
    var corntab_weekday_val = document.getElementById('corntab_weekday_val');

    noUiSlider.create(corntab_weekday, {
        start: [0],
        connect: 'lower',
        range: {
            'min': [0],
            'max': [7]
        }
    });
    corntab_weekday.noUiSlider.on('update', function (values, handle) {
        corntab_weekday_val.innerHTML = values[handle].split('.')[0]; //.split('.')[0]  从点开始,全部去掉，0表示全部去掉，点表示从点开始
    });


    // DEFAULT RANGE SLIDER Minute
    var corntab_minute = document.getElementById('corntab_minute');
    var corntab_minute_val = document.getElementById('corntab_minute_val');
    noUiSlider.create(corntab_minute, {
        start: [0],
        connect: 'lower',
        range: {
            'min': [0],
            'max': [59]
        }
    });
    corntab_minute.noUiSlider.on('update', function (values, handle) {
        corntab_minute_val.innerHTML = values[handle].split('.')[0]; //.split('.')[0]  从点开始,全部去掉，0表示全部去掉，点表示从点开始
    });


    // DEFAULT RANGE SLIDER Hour
    var corntab_hour = document.getElementById('corntab_hour');
    var corntab_hour_val = document.getElementById('corntab_hour_val');
    noUiSlider.create(corntab_hour, {
        start: [1],
        connect: 'lower',
        range: {
            'min': [0],
            'max': [23]
        }
    });
    corntab_hour.noUiSlider.on('update', function (values, handle) {
        corntab_hour_val.innerHTML = values[handle].split('.')[0]; //.split('.')[0]  从点开始,全部去掉，0表示全部去掉，点表示从点开始
    });

    //defaults
    $.fn.editable.defaults.mode = 'popup';
    //x-edit periodic taskname history
    $("#periodic_task_name_history").editable({
        url: "/post",
        type: "text",
        pk: 1,
        name: "username",
        title: "Enter username"
    });

});





