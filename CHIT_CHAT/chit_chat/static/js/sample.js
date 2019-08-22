$("document").ready(function () {
    fetch(user_url)
        .then(response => response.json())
        .then(result => renderUsers(result))
        .then(users => getMessage(users))
        .catch(err => console.log(err));

});


function renderUsers(users) {
    let user_id_arr = [];
    let user_profile_pic = [];
    users.forEach(function (item, index) {
        let id = item['id'];
        user_id_arr.push(id);
        let display_name = item['username'];
        let profile_pic = item['profile_pic'];
        user_profile_pic[index] = profile_pic;

        if (id == user) {
            $(".logged-in-user").find(".user_info").find(".user_name").html("HELLO " + display_name);
            if (profile_pic) {
                $(".logged-in-user").find(".user_img").attr("src", profile_pic);
            }
        } else if (id != user) {
            let user_id = "#" + id;
            $("#user_details").clone().removeClass('d-none').appendTo("ui.contacts").attr("id", id);
            $("#" + id).find(".user_info").find(".user_name").html(display_name);
            if (profile_pic) {
                $("#" + id).find(".user_img").attr("src", profile_pic);
            }
        }
    });
    localStorage.setItem("profile_pic_arr", JSON.stringify(user_profile_pic));

    return user_id_arr;
}

function getMessage(users) {

    users.forEach(function (item, index) {
        if (user != item) {
            let user_ids = "#" + item;

            $(user_ids).on('click', function (event) {

                let body_children = $(".msg_card_body").children();

                let body_len = body_children.length;

                for (let i = 0; i < body_len; i++) {
                    if ($(body_children[i]).attr("class") !== 'd-none') {
                        $(body_children[i]).remove();
                    }
                }


                let element = event.currentTarget;
                let client = $(element).attr("id");
                localStorage.setItem("client", client);
                let new_msg_url = msg_url + "?userid=" + client;

                localStorage.setItem("photo_index", index);

                fetch(new_msg_url)
                    .then(response => response.json())
                    .then(result => renderMessage(result, index))
                    .then((client) => writeMessage())
                    .catch(err => console.log(err));

                keepRendering(new_msg_url, client);
            });
        }
    });
}


function renderMessage(msg) {
    let content_len = msg.length;
    localStorage.setItem("content_len", content_len);
    let client = localStorage.getItem("client");
    let len = Object.keys(msg).length - 1;
    let profile_pic_arr = JSON.parse(localStorage.getItem("profile_pic_arr"))
    // console.log(profile_pic_arr);
    let photo_index = localStorage.getItem("photo_index");
    console.log(photo_index);

    if (profile_pic_arr[photo_index]) {
        console.log($(".chat-box-img"));
        $(".chat-box-img").attr("src", profile_pic_arr[photo_index]);
    }

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

    let sender_ele = $("#sender" + len);
    let receiver_ele = $("#receiver" + len);
    if (sender_ele.length) {
        sender_ele[0].scrollIntoView();
    } else {
        receiver_ele[0].scrollIntoView();
    }
    return client;
}


function writeMessage() {

    $("#submit_chat").on("click", function () {
        let text_area = $("#type_msg");
        text_area.blur();
        let csrf_token = $('.csrf-send-msg > input[name="csrfmiddlewaretoken"]').val();
        let client = localStorage.getItem("client");
        console.log(client);
        if (text_area.val() !== "") {
            let data = {text_msg: text_area.val(), receiver: client};
            text_area.val("");

            fetch(msg_url, {
                method: 'POST',
                body: JSON.stringify(data),
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrf_token
                }
            })
                .then(response => response.json())
                .then(result => {
                    let msg = [result];
                    appendMessage(msg)
                })
                .catch(err => console.log(err));
        }
    });
}


function appendMessage(msg) {

    for (let i = 0; i < msg.length; i++) {
        let txt_msg = msg[i]['text_msg'];
        let content_length = localStorage.getItem("content_len");
        let client = localStorage.getItem("client");
        // console.log(client);
        // console.log(msg[i]['receiver']);
        if (msg[i]['sender'] == user && msg[i]['receiver'] == client) {
            console.log("hi");
            $("#sender").clone().removeClass('d-none').appendTo(".msg_card_body").find(".msg_cotainer_send").html(txt_msg);

            content_length = Number(content_length) + 1;
            localStorage.setItem("content_len", content_length);
        } else if (msg[i]['sender'] == client) {
            $("#receiver").clone().removeClass('d-none').appendTo(".msg_card_body").find(".msg_cotainer").html(txt_msg);

        }
    }

}


function keepRendering(new_msg_url, client) {

    setInterval(function () {
        fetch(new_msg_url)
            .then(response => response.json())
            .then(result => {

                let content_len = localStorage.getItem("content_len");
                let res_len = result.length;
                let client = localStorage.getItem("client");
                // console.log(client);


                let new_result = [];
                if (content_len < res_len) {

                    for (let i = content_len; i < res_len; i++) {
                        new_result.push(result[i]);
                    }
                    appendMessage(new_result);
                    localStorage.setItem("content_len", res_len);
                }
            })
            .catch(err => console.log(err));
    }, 2000);
}


function confirmEnter() {

    let key = window.event.keyCode;
    if (key === 13) {
        $("#submit_chat").click();
        return false;
    } else {
        return true;
    }
}