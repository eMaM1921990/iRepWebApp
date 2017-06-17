/**
 * Created by mac on 4/8/17.
 */
function changeAppLanguage(langCode){
    $.ajax({
        url: "/i18n/setlang/",
        type: 'POST',
        data:{
            language:langCode,
            next:'/',
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
        },
        success: function (responseText) {
               window.location.reload();
        },
        error: function (xhr, errmsg, err) {
            console.log(errmsg);
        }
    });
}


function success_behavior(responseText){
    $('#success #msg').html(JSON.parse(responseText).msg);
    $('#success').removeAttr('style');
    $("#success").fadeOut(3000);
}

function error_behavior(responseText){
    $('#error #msg').html(JSON.parse(responseText).msg);
    $('#error').removeAttr('style');
    $("#error").fadeOut(3000);
}
