/**
 * Created by mac on 7/3/17.
 */



$("#button-id-apply").click(function (event) {
    event.preventDefault();
     var vFD = new FormData(document.getElementById('sales-force-form-report-id'));

     $.ajax({
        url: "/report/visit_tracking_by_sales_force/",
        cache: false,
        contentType: false,
        processData: false,
        type: 'POST',
        //dataType: 'JSON',
        data:vFD,
        success: function (responseText) {
            $('#from_date').text(vFD.get('date_from'));
            $('#to_date').text(vFD.get('date_to'));
               if(JSON.parse(responseText).valid){
                   $('#tracking tr:last').after(JSON.parse(responseText).html);
               }else {

               }
        },
        error: function (xhr, errmsg, err) {
            console.log(errmsg);
        }
    });

});