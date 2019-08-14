$("document").ready(function () {
    fetch(user_url)
        .then(response => response.json())
        .then(result => renderUsers(result))
        .then(users => getMessage(users))
        .catch(err => console.log(err));

});


function renderUsers(users) {
    let user_id_arr = [];
    users.forEach(function (item, index) {
        let id = item['id'];
        user_id_arr.push(id);
        let display_name = item['username'];
        if (id != user) {
            let user_id = "#" + id;
            $("#user_details").clone().removeClass('d-none').appendTo("ui.contacts").attr("id", id);
            $("#" + id).find(".user_info").find(".user_name").html(display_name);
            return users;
        }
    });

    return user_id_arr;
}

function getMessage(users) {
    users.forEach(function (item, index) {
        if (user != item) {
            let user_ids = "#" + item;

            $(user_ids).on('click', function (event) {

                let body_children = $(".msg_card_body").children();
                let body_len = body_children.length;

                for (i = 0; i < body_len; i++) {
                    if ($(body_children[i]).attr("class") !== 'd-none') {
                        $(body_children[i]).remove();
                    }
                }


                // body_children.forEach(function(item,index) {
                //     if($(item).attr("class") !== 'd-none'){
                //         $(item).remove();
                //     }
                // });

                let element = event.currentTarget;
                let client = $(element).attr("id");
                localStorage.setItem("client", client);
                let new_msg_url = msg_url + "?userid=" + client;

                fetch(new_msg_url)
                    .then(response => response.json())
                    .then(result => renderMessage(result))
                    .then((client) => writeMessage(client))
                    .catch(err => console.log(err));
            });
        }
    });
}


function renderMessage(msg) {
    let client = localStorage.getItem("client");

    msg.forEach(function (item, index) {
        let txt_msg = item['text_msg'];
        let sender_user = item['sender'];
        let receiver_user = item['receiver'];


        if (sender_user == user && receiver_user == client) {
            $("#sender").clone().removeClass('d-none').appendTo(".msg_card_body").attr("id", "sender" + index);
            $("#sender" + index).find(".msg_cotainer_send").html(txt_msg);
        } else if (sender_user == client) {
            $("#receiver").clone().removeClass('d-none').appendTo(".msg_card_body").attr("id", "receiver" + index);
            $("#receiver" + index).find(".msg_cotainer").html(txt_msg);
        }
    });
    return client;
}


function writeMessage(client) {

    $("#submit_chat").on("click", function () {

        let data = {text_msg: $("#type_msg").val(), receiver: client};
        $("#type_msg").val("");

        fetch(msg_url, {
            method: 'POST',
            body: JSON.stringify(data),
            headers: {'Content-Type': 'application/json'}
        })
            .then(response => response.json())
            .then(result => appendMessage(result))
            .catch(err => console.log(err));
    });
}


function appendMessage(msg) {
    
    let txt_msg = msg['text_msg'];
    $("#sender").clone().removeClass('d-none').appendTo(".msg_card_body").find(".msg_cotainer_send").html(txt_msg);
}


function confirmEnter() {

    var key = window.event.keyCode;
    if (key === 13) {
        $("#submit_chat").click();
        return false;
    } else {
        return true;
    }
}