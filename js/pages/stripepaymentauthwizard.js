
var FormsWizard = function() {

    return {
        init: function() {

            /* Initialize Advanced Wizard with Validation */
            $('#advanced-wizard').formwizard({
                disableUIStyles: true,
                validationEnabled: true,
                validationOptions: {
                    errorClass: 'help-block animation-slideDown', // You can change the animation class for a different entrance animation - check animations page
                    errorElement: 'span',
                    errorPlacement: function(error, e) {
                        e.parents('.form-group > div > div').append(error);
                    },
                    highlight: function(e) {
                        $(e).closest('.form-group').removeClass('has-success has-error').addClass('has-error');
                        $(e).closest('.help-block').remove();
                    },
                    success: function(e) {
                        // You can use the following if you would like to highlight with green color the input after successful validation!
                        e.closest('.form-group').removeClass('has-success has-error'); // e.closest('.form-group').removeClass('has-success has-error').addClass('has-success');
                        e.closest('.help-block').remove();
                    },
                    rules: {
                        inputPhoneNumber: {
                            required: true,
                            minlength: 12
                        },
                        inputStreetAddress: {
                            required: true,
                            minlength: 3
                        },
                        inputCity: {
                            required: true,
                            minlength: 3
                        },
                        select_state: {
                            required: true,
                            minlength: 1
                        },
                        inputZip: {
                            required: true,
                            minlength: 5
                        },
                        select_dobday: {
                            required: true,
                            minlength: 1
                        },
                        select_dobmonth: {
                            required: true,
                            minlength: 1
                        },
                        inputDOBYear: {
                            required: true,
                            minlength: 4
                        },
                        inputLast4SSN: {
                            required: true,
                            minlength: 4
                        },
                        inputCheckingAccountRoutingNumber: {
                            required: true,
                            minlength: 1
                        },
                        inputCheckingAccountNumber: {
                            required: true,
                            minlength: 1
                        },
                        stripeToken: {
                            required: true,
                            minlength: 1
                        }
                    },
                    messages: {
                        inputPhoneNumber: {
                            required: 'Please provide your phone number',
                            minlength: 'Your phone number should be 10 digits long'
                        },
                        inputStreetAddress: {
                            required: 'Please provide your street address',
                            minlength: 'Your street address must consist of at least 3 characters'
                        },
                        inputCity: {
                            required: 'Please provide your city',
                            minlength: 'Your city must consist of at least 3 characters'
                        },
                        select_state: {
                            required: 'Please select your state',
                            minlength: 'Please select your state'
                        },
                        inputZip: {
                            required: 'Please provide your zip code',
                            minlength: 'Your zip code should be 5 digits long'
                        },
                        select_dobday: {
                            required: 'Please provide the day of your birthday',
                            minlength: 'Your birth day should be at least 1 digits long'
                        },
                        select_dobmonth: {
                            required: 'Please provide the month of your birthday',
                            minlength: 'Your birth month should be at least 1 digits long'
                        },
                        inputDOBYear: {
                            required: 'Please provide the year of your birthday',
                            minlength: 'Your birth year should be 4 digits long'
                        },
                        inputLast4SSN: {
                            required: 'Please provide the last 4 digits of your SSN #',
                            minlength: 'Your last 4 digits of your SSN # should be 4 digits long'
                        },
                        inputCheckingAccountRoutingNumber: {
                            required: 'Please provide the routing number for your checking account',
                            minlength: 'Please provide the routing number for your checking account'
                        },
                        inputCheckingAccountNumber: {
                            required: 'Please provide the account number for your checking account',
                            minlength: 'Please provide the account number for your checking account'
                        },
                        stripeToken: {
                            required: 'Please validate your checking account',
                            minlength: 'Please validate your checking account'
                        }
                    }
                },
                inDuration: 0,
                outDuration: 0
            });

        }
    };
}();