/**
 * Created by mac on 8/29/17.
 */
$('#saveCategoryBtn').on('click', function (event) {
    var vFD = new FormData(document.getElementById('saveCategory'));

    $.ajax({
        url: "/settings/category/add/",
        cache: false,
        contentType: false,
        processData: false,
        type: 'POST',
        //dataType: 'JSON',
        data: vFD,
        success: function (responseText) {
            console.log(JSON.parse(responseText));
            if (JSON.parse(responseText).valid) {

                $('#id_product').append($('<option></option>').val(JSON.parse(responseText).objects.id).html(JSON.parse(responseText).objects.name));
            }

            $('#productCategory').modal('hide');
            $('#saveCategory').trigger('reset');

        },
        error: function (xhr, errmsg, err) {
            console.log(errmsg);
        }
    });
});