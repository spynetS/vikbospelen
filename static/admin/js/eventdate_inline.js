document.addEventListener("DOMContentLoaded", function() {

    var $ = window.django && django.jQuery ? django.jQuery : window.$;
    if (!$) return;

    function toggleFields(row) {
        var yearOnly = row.find('input[name$="-year_only"]');
				

        // Find datetime inputs by ID pattern (date & time)
        var datetimeTd = row.find('td:has(input[id*="-datetime_"])');
        var yearTd = row.find('input[name$="-year"]').closest('td');
				row.find('input[name$="-year"]').attr("placeholder", "År")
				
        if (yearOnly.is(':checked')) {
            datetimeTd.hide(); // hide full datetime widget
            yearTd.show();
        } else {
            datetimeTd.show();
            yearTd.hide();
        }
    }

    // Initial toggle for existing inline rows
    $('tr.form-row').each(function() {
        toggleFields($(this));
    });

    // Toggle dynamically when checkbox changes
    $(document).on('change', 'input[name$="-year_only"]', function() {
        toggleFields($(this).closest('tr'));
    });

    // Handle dynamically added inline rows
    $(document).on('formset:added', function(event, row) {
        toggleFields($(row));
    });
});
