$("document").ready(function () {

    window.counter = [];
    window.flag = false;
    fetch(user_url)
        .then(response => response.json())
        .then(result => renderUsers(result))
        .catch(err => console.log(err));


    setInterval(function () {
        fetch(user_url)
            .then(response => response.json())
            .then(result => renderUsers(result))
            .catch(err => console.log(err));
    }, 2000);

});


function renderUsers(users) {

    let user_id_arr = [];
    let user_profile_pic = [];

    let user_len = users.length;
    let sorted_users = null;
    for (let i = 0; i < user_len; i++) {
        if (users[i]['id'] == user) {

            sorted_users = users[i]['last_msg'];
            let display_name = users[i]['username'];
            let profile_pic = users[i]['profile_pic'];
            $(".logged-in-user").find(".user_info").find(".user_name").html(display_name);
            if (profile_pic) {
                $(".logged-in-user").find(".user_img").attr("src", profile_pic);
            }
            break;
        }
    }


    sorted_users = sorted_users.sort(function (a, b) {
        return b.val.localeCompare(a.val);
    });

    let sorted_user_id = [];
    let sorted_date_time = [];
    sorted_users.forEach(function (item, index) {
        let date = new Date(item['val']);
        date = date.toLocaleString();
        sorted_date_time.push(date);
        sorted_user_id.push(item['key']);
    });

    let sorted_array = [];
    for (let i = 0; i < sorted_user_id.length; i++) {
        for (let j = 0; j < users.length; j++) {
            if (users[j]['id'] === sorted_user_id[i]) {
                sorted_array.push(users[j]);
                users.splice(j, 1);
            }
        }
    }

    let final_sorted_array = sorted_array.concat(users);

    let old_sorted_array = JSON.parse(localStorage.getItem("final_sorted_array"));


    if (old_sorted_array && old_sorted_array[0]['id'] !== final_sorted_array[0]['id'] && window.flag) {


        let body_children = $(".contacts").children();


        let body_len = body_children.length;

        for (let i = 0; i < body_len; i++) {
            if ($(body_children[i]).attr("id") !== 'user_details') {
                $(body_children[i]).remove();
            }
        }


        user_id_arr = listUsers(final_sorted_array, user_profile_pic, sorted_date_time);

        getMessage(user_id_arr);

    } else if (!window.flag) {
        window.flag = true;

        user_id_arr = listUsers(final_sorted_array, user_profile_pic, sorted_date_time);
        getMessage(user_id_arr);
    }

    localStorage.setItem("final_sorted_array", JSON.stringify(final_sorted_array));


    return user_id_arr;
}


function listUsers(final_sorted_array, user_profile_pic, sorted_date_time) {
    let user_id_arr = [];
    let username_arr = [];
    final_sorted_array.forEach(function (item, index) {

        let username = item['username'];
        let id = item['id'];
        let profile_pic = item['profile_pic'];
        let last_msg_time = null;
        let display_name = item['username'];
        user_profile_pic[index] = profile_pic;


        user_id_arr.push(id);
        username_arr.push(username);


        if (sorted_date_time[index]) {
            last_msg_time = sorted_date_time[index];
        } else {
            last_msg_time = "No previous conversations"
        }


        if (id != user) {

            $("#user_details").clone().removeClass('d-none').appendTo("ui.contacts").attr("id", id);
            $("#" + id).find(".user_info").find(".user_name").html(display_name);

            $("#" + id).find(".user_info").find(".last-msg-time").html(last_msg_time);

            if (profile_pic) {
                $("#" + id).find(".user_img").attr("src", profile_pic);
            }
        }

        if (username == $(".display-chat-name").html()) {
            $('#' + id).addClass("background-on-select");
        }

        localStorage.setItem("profile_pic_arr", JSON.stringify(user_profile_pic));
    });
    localStorage.setItem("username_arr", JSON.stringify(username_arr));
    return user_id_arr;
}


function getMessage(users) {
    let username_arr = JSON.parse(localStorage.getItem("username_arr"));
    users.forEach(function (item, index) {
        if (user != item) {
            let username = username_arr[index];
            let user_ids = "#" + item;
            window.counter.push(item);

            $(user_ids).on({'click': (event) => clickEvents(event, index, user_ids, username)}
            );
        }
    });
}


function clickEvents(event, index, user_ids, username) {

    if ($(".display-chat-name").html() == username) {
        return false;
    }

    if ($(window).width() < 992) {
        $("#contact-display").css("display", "none");
        $("#message-display").css("display", "block");
        $(".fa-arrow-left").css("display", "block");

        $(".fa-arrow-left").on("click", function () {
            $("#message-display").css("display", "none");
            $("#contact-display").css("display", "block");
        });
    }

    $(".contacts li").removeClass("background-on-select");
    $(user_ids).addClass("background-on-select");

    let body_children = $(".msg_card_body").children();

    let body_len = body_children.length;

    for (let i = 0; i < body_len; i++) {
        if ($(body_children[i]).attr("class") !== 'd-none') {
            $(body_children[i]).remove();
        }
    }

    $(".no-conversation-render").addClass("d-none");
    $(".msg-render").removeClass("d-none");


    let element = event.currentTarget;
    let client = $(element).attr("id");
    localStorage.setItem("client", client);
    let new_msg_url = msg_url + "?userid=" + client;

    localStorage.setItem("photo_index", index);

    fetch(new_msg_url)
        .then(response => response.json())
        .then((result) => renderMessage(result, index, username))
        .then((client) => keepRendering(new_msg_url, client))
        .catch(err => console.log(err));

    writeMessage();
}


function renderMessage(msg, index, username) {

    let client = localStorage.getItem("client");

    if ($(".display-chat-name").html() == username) {
        return client;
    }

    clearInterval(window.rendering);

    let content_len = msg.length;
    localStorage.setItem("content_len", content_len);


    let len = Object.keys(msg).length - 1;
    let profile_pic_arr = JSON.parse(localStorage.getItem("profile_pic_arr"));
    let photo_index = localStorage.getItem("photo_index");

    $(".display-chat-name").html(username);

    if (profile_pic_arr[photo_index]) {
        $(".chat-box-img").attr("src", profile_pic_arr[photo_index]);
    }

    msg.forEach(function (item, index) {
        let txt_msg = item['text_msg'];

        let sender_user = item['sender'];
        let receiver_user = item['receiver'];


        if (sender_user == user && receiver_user == client) {
            $("#sender").clone().removeClass('d-none').appendTo(".msg_card_body").attr("id", "sender" + index).find(".msg_cotainer_send > span").html(txt_msg);

        } else if (sender_user == client) {
            $("#receiver").clone().removeClass('d-none').appendTo(".msg_card_body").attr("id", "receiver" + index).find(".msg_cotainer > span").html(txt_msg);

        }

    });

    let sender_ele = $("#sender" + len);
    let receiver_ele = $("#receiver" + len);
    if (sender_ele.length) {
        sender_ele[0].scrollIntoView();
    } else if (receiver_ele.length) {
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
        let new_element;
        if (msg[i]['sender'] == user && msg[i]['receiver'] == client) {
            console.log("1");
            $("#sender").clone().removeClass('d-none').appendTo(".msg_card_body").find(".msg_cotainer_send > span").attr("id", "new_msg").html(txt_msg);
            content_length = Number(content_length) + 1;
            localStorage.setItem("content_len", content_length);
        } else if (msg[i]['sender'] == client) {
            console.log("2");
            $("#receiver").clone().removeClass('d-none').appendTo(".msg_card_body").find(".msg_cotainer > span").attr("id", "new_msg").html(txt_msg);
        }
        console.log("3");
        if ($("#new_msg").length > 0) {
            $("#new_msg")[0].scrollIntoView();
            $("#new_msg").removeAttr("id");
        }

    }

}


function keepRendering(new_msg_url, client) {


    window.rendering = setInterval(function () {
        fetch(new_msg_url)
            .then(response => response.json())
            .then(result => {

                let content_len = localStorage.getItem("content_len");
                let res_len = result.length;


                let new_result = [];
                if (content_len < res_len) {

                    for (let i = content_len; i < res_len; i++) {
                        new_result.push(result[i]);
                    }
                    localStorage.setItem("content_len", res_len);
                    appendMessage(new_result);
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