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
        var txt = $("#reject-reason").val();
        if (txt == "") {
            alert("Пожалуйста, введите причину отказа");
            return;
        }
        $.ajax("/api/individual/" + individual_id + "/ops/prescoring_reject/", {
            data: JSON.stringify({"payload": txt}),
            contentType: 'application/json',
            type: 'POST'
        });
        $('#rejectModal').modal('hide');
        location.reload();
    });

    $(".show_payload").click(function () {
        var data = jQuery(this).attr("custom_tag");
        $("#myModal #modal-content-main").html(data);
        $('#myModal').modal('show');

    });

    $(".img-custom").click(function () {
        var data = jQuery(this).attr('src');
        $("#myModal #modal-content-main").html("<img src=\"" + data + "\"class='img-modal'/>");
        $('#myModal').modal('show');

    });

    $("#prescoring-decline").click(function () {
        var data = jQuery(this).attr("custom_tag");
        $("#rejectModal #modal-content-main").html(data);
        $('#rejectModal').modal('show');

    });


    if (typeof individual_id != "undefined") {
        $.getJSON('/api/individual/' + individual_id + "/current_generation/state/", function (data) {
            if (data['scoring_start'] == false)
                $("#scoring-button").addClass("disabled");
            if (data['prescoring_decline'] == false)
                $("#prescoring-decline").addClass("disabled");
            if (data['generation_next'] == false)
                $("#new-generation").addClass("disabled");
            if (data['postscoring_accept'] == false)
                $("#accept-individual").addClass("disabled");
            if (data['postscoring_reject'] == false)
                $("#reject-individual").addClass("disabled");
            if (data['results'] == false)
                $("#scoring_results").addClass("disabled");
        });
    }


});