$(document).ready(function () {
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

// set csrf header
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", window.CSRF_TOKEN);
            }
        }
    });
    $("#reject-button").click(function () {

        var text = $('textarea#textform').val();
        $.ajax("/api/client/1/add_action/", {
            data: JSON.stringify({"processor": "User", "action_type": "manual_decline", "payload": text}),
            contentType: 'application/json',
            type: 'POST'
        });

        alert('Отказ по клиенту сохранен.');
    });

    $("#scoring-button").click(function () {


        $.ajax("/api/message/", {
            data: JSON.stringify({
                "message_type": "individual_scoring_process",
                "body": JSON.stringify({"individual_id": individual_id, "product_id": product_id})
            }),
            contentType: 'application/json',
            type: 'POST'
        });

        alert('Клиент отправлен на скоринг.');
    });

});