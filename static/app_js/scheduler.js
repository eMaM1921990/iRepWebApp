/**
 * Created by mac on 6/17/17.
 */

function addSchedular() {
    var vFD = new FormData(document.getElementById('schedualer-form'));

    $.ajax({
        url: "/scheduler/add/",
        cache: false,
        contentType: false,
        processData: false,
        type: 'POST',
        //dataType: 'JSON',
        data: vFD,
        success: function (responseText) {
            if (JSON.parse(responseText).valid) {
                $('#myModal').modal('hide');
                $('#schedualer-form').trigger('reset');
                addToCalendeer('new_visit',vFD.get('dates'));
            } else {

            }
        },
        error: function (xhr, errmsg, err) {
            console.log(errmsg);
        }
    });
}


function editSchedular(event_id) {
    var vFD = new FormData(document.getElementById('schedualer-form-edit'));
    $.ajax({
        url: "/scheduler/edit/",
        cache: false,
        contentType: false,
        processData: false,
        type: 'POST',
        //dataType: 'JSON',
        data: vFD,
        success: function (responseText) {
            if (JSON.parse(responseText).valid) {
                $('#myModaledit ').modal('hide');
                $('#schedualer-form').trigger('reset');
                removeFromCalender(event_id);
                addToCalendeer('new_visit',vFD.get('dates'));
            } else {

            }
        },
        error: function (xhr, errmsg, err) {
            console.log(errmsg);
        }
    });
}



function addToCalendeer(visit_name, date) {
    var myCalendar = $('#calendar');
    myCalendar.fullCalendar();
    var myEvent = {
        title: visit_name,
        allDay: true,
        start: new Date(date),
        end: new Date(date)
    };
    myCalendar.fullCalendar('renderEvent', myEvent);

}


function removeFromCalender(id){
    var myCalendar = $('#calendar');
    myCalendar.fullCalendar( 'removeEvents' , id);
}

function deleteSchedular(event_id) {
    var vFD = new FormData(document.getElementById('schedualer-form-edit'));
    $.ajax({
        url: "/scheduler/delete/",
        cache: false,
        contentType: false,
        processData: false,
        type: 'POST',
        //dataType: 'JSON',
        data: vFD,
        success: function (responseText) {
            if (JSON.parse(responseText).valid) {
                $('#myModaledit ').modal('hide');
                $('#schedualer-form').trigger('reset');
                removeFromCalender(event_id);
                // addToCalendeer('new_visit',vFD.get('dates'));
            } else {

            }
        },
        error: function (xhr, errmsg, err) {
            console.log(errmsg);
        }
    });
}

