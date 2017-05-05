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
