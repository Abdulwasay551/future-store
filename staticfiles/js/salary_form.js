(function($) {
    $(document).ready(function() {
        const employeeSelect = $('#id_employee');
        
        function updateFields() {
            const employeeId = employeeSelect.val();
            if (!employeeId) return;

            // Fetch employee data
            $.get(`/admin/api/employee/${employeeId}/details/`, function(data) {
                if (data.employee_finance) {
                    $('#id_employee_finance').val(data.employee_finance.id);
                }
                
                if (data.active_loan) {
                    $('#id_loan_deduction').val(data.active_loan.per_month_deduction);
                }

                if (data.employee_finance && data.employee_finance.base_salary > 50000) {
                    $('#id_tax_deduction').val(data.employee_finance.base_salary * 0.1);
                }
                
                // Allow manual override
                $('#id_employee_finance, #id_loan_deduction, #id_tax_deduction').prop('readonly', false);
            });
        }

        employeeSelect.on('change', updateFields);
        
        // Initial load
        if (employeeSelect.val()) {
            updateFields();
        }
    });
})(django.jQuery);
