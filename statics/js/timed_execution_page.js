// Form-Component.js
// ====================================================================
// This file should not be included in your project.
// This is just a sample how to initialize plugins or components.
$(document).on('nifty.ready', function () {


    // CHOSEN TIME ZONE
    $('#demo-chosen-select').chosen();
    // BOOTSTRAP DATEPICKER WITH AUTO CLOSE
    $('#demo-dp-component .input-group.date').datepicker({autoclose: true});
    // BOOTSTRAP TIMEPICKER
    $('#demo-tp-com').timepicker();

});

