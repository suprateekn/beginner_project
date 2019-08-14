$("document").ready(function () {

    $.ajax({
        type: "GET",
        url: user_url,
        success: function (data) {
            count = Object.keys(data).length;
            var j = 0;
            for (var i = 0; i < count; i++) {
                var id = data[i]['id'];
                var display_name = data[i]['username'];
                if (user != id) {
                    var user_ids = "#" + id;
                    $("#user_details").clone().removeClass('d-none').appendTo("ui.contacts").attr("id", id);
                    $(user_ids).find(".user_info").find(".user_name").html(display_name);
                    console.log($(user_ids));
                    $(user_ids).on('click', function (event) {
                        body_children = $(".msg_card_body").children();
                        body_len = body_children.length;
                        for (var i = 0; i < body_len; i++) {
                            if ($(body_children[i]).attr("class") !== 'd-none') {
                                $(body_children[i]).remove();
                            }
                        }


                        var element = event.currentTarget;
                        var client = $(element).attr("id");
                        var new_msg_url = msg_url + "?userid=" + client;

                        $('#sender_user_id').val(client);

                        $.ajax({
                            type: "GET",
                            url: new_msg_url,
                            success: function (msg) {
                                len = Object.keys(msg).length;
                                for (i = 0; i < len; i++) {
                                    var txt_msg = msg[i]['text_msg'];
                                    var sender_user = msg[i]['sender'];
                                    var receiver_user = msg[i]['receiver'];


                                    if (sender_user == user && receiver_user == client) {
                                        $("#sender").clone().removeClass('d-none').appendTo(".msg_card_body").attr("id", "sender" + i);
                                        $("#sender" + i).find(".msg_cotainer_send").html(txt_msg);
                                    } else if (sender_user == client) {
                                        $("#receiver").clone().removeClass('d-none').appendTo(".msg_card_body").attr("id", "receiver" + i);
                                        $("#receiver" + i).find(".msg_cotainer").html(txt_msg);
                                    }
                                }
                            }
                        });
                    });
                }
            }
        }
    });
    $("#submit_chat").on('click', function () {

        $.ajax({
            type: "POST",
            url: msg_url,
            data: {text_msg: $("#type_msg").val(), receiver: $("#sender_user_id").val()},
            success: function (msg) {
                $("#type_msg").val("");
                let sender_user = msg['sender'];
                let receiver_user = msg['receiver'];
                let txt_msg = msg['text_msg'];

                if (sender_user == user) {
                    $("#sender").clone().removeClass('d-none').appendTo(".msg_card_body").find(".msg_cotainer_send").html(txt_msg);
                }
            },
            error: function (err) {
                console.log(err);
            }
        });
    });
});

function confirmEnter() {

    var key = window.event.keyCode;
    if (key === 13) {
        $("#submit_chat").click();
        return false;
    } else {
        return true;
    }
}