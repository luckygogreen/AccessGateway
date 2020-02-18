// Form-Component.js
// ====================================================================
// This file should not be included in your project.
// This is just a sample how to initialize plugins or components.
$(document).on('nifty.ready', function () {


    // CHOSEN
    $('#demo-chosen-select').chosen();
    // BOOTSTRAP DATEPICKER WITH AUTO CLOSE
    $('#demo-dp-component .input-group.date').datepicker({autoclose: true});
    // BOOTSTRAP TIMEPICKER
    $('#demo-tp-com').timepicker();


    // DEFAULT RANGE SLIDER
    var rs_def = document.getElementById('demo-range-def');
    var rs_def_value = document.getElementById('demo-range-def-val');

    noUiSlider.create(rs_def, {
        start: [5],
        connect: 'lower',
        range: {
            'min': [1],
            'max': [100]
        }
    });

    rs_def.noUiSlider.on('update', function (values, handle) {
        rs_def_value.innerHTML = values[handle].split('.')[0]; //.split('.')[0]  从点开始,全部去掉，0表示全部去掉，点表示从点开始
    });


});

