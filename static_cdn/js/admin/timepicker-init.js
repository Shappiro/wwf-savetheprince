$ = django.jQuery

$(document).ready(function () {
    $('.timepicker').clockTimePicker({
        alwaysSelectHoursFirst: true,
        afternoonHoursInOuterCircle: true,
        //duration: true,
        //durationNegative: true,
        //precision: 5,
        //i18n: {
        //    cancelButton: 'Abbrechen'
        //},
    });
});