$(document).ready(function () {
    $(".shorten_payload").shorten({
        moreText: 'Раскрыть',
        lessText: 'Скрыть'
    });
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

    $(".check-scoring").click(function () {

        $.ajaxSetup({
            async: false
        });
        var id = jQuery(this).attr("custom_id");
        var gen = jQuery(this).attr("custom_gen");
        status = true;
        $.getJSON({
            url: "/api/individual/" + id + "/" + gen + "/data/scoring/",
            async: false,
            success: function (data, textstatus, jqXHR) {
                if (jqXHR.status != 200 || jQuery.isEmptyObject(data)) {
                    status = false;
                }
            }
        });
        if (status == "false") {
            alert("В версии данных отсутствуют данные скоринга.");
            event.preventDefault();
            return false;
        }
        return true;
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

    $("#new-generation").click(function () {
        return confirm("Вы уверены, что хотите отправить досье в архив?");
    });


    $("#show-raw-data").click(function () {
        var dt = "";
        $.getJSON('/api/individual/' + individual_id + "/cur_gen/data/source", function (data) {
            dt = JSON.stringify(data);
            //  $("").html(dt);
            $('#showRawDataModal #modal-content-main').jsonViewer(data, {
                collapsed: true,
                withQuotes: true,
                withLinks: false
            });
            $('#showRawDataModal').modal('show');
        });


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
            if (data['results'] == false) {
                $("#scoring_results").addClass("disabled");
                $("#scoring_report").addClass("disabled");
            }

            var timeout;
            if (window.location.pathname.includes("individual_inspect")) {
                if (data['scoring_start'] == false && data['prescoring_decline'] == false && data['generation_next'] == false && data['postscoring_accept'] == false && data['postscoring_reject'] == false && data['results'] == false) {
                    timeout = setTimeout(function () {
                        window.location.reload();
                    }, 2000);
                }
                else {
                    if (timeout != "undefined")
                        clearTimeout(timeout);
                }
            }
        });
    }


});

