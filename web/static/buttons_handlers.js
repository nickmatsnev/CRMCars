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

        var text = $('#reject-reason').val();
        // $.ajax("/api/client/" + client_id + "/ops/prescoring_reject/", {
        //     data: JSON.stringify({"payload": text}),
        //     contentType: 'application/json',
        //     type: 'POST'
        // });


        $('#rejectModal').modal('hide');
        location.reload()
    });

    $(".show_payload").click(function () {
        var data = jQuery(this).attr("custom_tag");
        $("#myModal #modal-content-main").html(data);
        $('#myModal').modal('show');

    });

    $("#prescoring_decline").click(function () {
        alert("click!!");
        var data = jQuery(this).attr("custom_tag");
        $("#rejectModal #modal-content-main").html(data);
        $('#rejectModal').modal('show');

    });


    $("#scoring-button").click(function () {
        $.getJSON('/api/individual/' + individual_id + "/ops/scoring_start/", function (data) {
        });
        //$.getJSON('/api/individual/' + individual_id + "/current_generation/state/", function (data) {
        //  if (data['scoring'] == true)
        //     $.getJSON('/api/individual/' + individual_id + "/ops/scoring_start/", function (data) {
        //  });
        //alert('Клиент отправлен на скоринг.');
        //});

    });

    if (typeof individual_id != "undefined") {
        $.getJSON('/api/individual/' + individual_id + "/current_generation/state/", function (data) {
            if (data['scoring'] == false)
                $("#scoring-button").addClass("disabled");
            if (data['prescoring_decline'] == false)
                $("#prescoring-decline").addClass("disabled");
            if (data['generation_next'] == false)
                $("#new-generation").addClass("disabled");
            if (data['postscoring_accept'] == false)
                $("#scoring-results").addClass("disabled");


            var items = [];
            //$.each(data, function(key, val) {
            //  items.push('<li id="' + key + '">' + val + '</li>');
            //});
        });
    }


});