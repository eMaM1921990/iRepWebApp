/**
 * Created by mac on 10/10/17.
 */
$("#button-id-apply").click(function (event) {
    event.preventDefault();
    var vFD = new FormData(document.getElementById('sales-force-form-report-id'));

    $.ajax({
        url: "/report/visit_tracking_by_client/",
        cache: false,
        contentType: false,
        processData: false,
        type: 'POST',
        //dataType: 'JSON',
        data: vFD,
        success: function (responseText) {
            $('#from_date').text(vFD.get('date_from'));
            $('#to_date').text(vFD.get('date_to'));
            $('#totalVisits').text(JSON.parse(responseText).visits);
            $('#totalOrder').text(JSON.parse(responseText).orders);


        },
        error: function (xhr, errmsg, err) {
            console.log(errmsg);
        }
    });

});



$("#fetch_from_answer").change(function (event) {
    event.preventDefault();

    $.ajax({
        url: "/forms/answer/",
        type: 'POST',
        //dataType: 'JSON',
        data: {
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
            id : $(this).val().split('-')[1],
            branch_id:$(this).val().split('-')[0]

        },
        success: function (responseText) {
            if(JSON.parse(responseText).valid){
                $('#form_answer').html();
                $('#form_answer').append(JSON.parse(responseText).html)
            }


        },
        error: function (xhr, errmsg, err) {
            console.log(errmsg);
        }
    });

});