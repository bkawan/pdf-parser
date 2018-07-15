$(function () {
    var inputs = ['file'];
    for (var i = 0; i < inputs.length; i++) {
        removeErrorOnKeyup(inputs[i])
    }

    // function to remove error on key up
    function removeErrorOnKeyup(inputName) {
        return $('input[name=' + inputName + ']').keyup(function (event) {
            $('#form-group-' + inputName).removeClass('has-error');
            $('#error-block-' + inputName).html('');
        });

    }


    // on submit document form
    var documentUploadForm = $('#document-upload-form');
    documentUploadForm.submit(function (event) {
        event.preventDefault();
        var formData = $(this).serializeArray();
        var url = $(this).attr('data-action-url');
        $.ajax({
            type: 'POST',
            url: url,
            data: formData,
            dataType: 'json',
            success: handleFormSuccess,
            error: handleFormError
        });
    });

    //This function handles the success on Ajax  post to on submit feedback form
    function handleFormSuccess(data, textStatus, jqXHR) {
        console.log('success')
    }

    //This function handles the error on Ajax  post
    // needs to display error for all the field  nicely
    function handleFormError(data, textStatus, errorThrown) {
        console.log('error')

        for (var i = 0; i < inputs.length; i++) {
            if (data.responseJSON.hasOwnProperty(inputs[i])) {
                var error = eval("data.responseJSON." + inputs[i] + "[0]");
                $('#form-group-' + inputs[i]).addClass('has-error');
                $('#error-block-' + inputs[i]).html(error)
            }
        }
    }

});