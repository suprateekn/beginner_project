$("document").ready(function () {
    fetch(user_url)
        .then(response => response.json())
        .then(result => renderUsers(result)).catch(err => console.log(err));

    // fetch(msg_url)
    // $
});


function renderUsers(users) {
    users.forEach(function (item, index) {
        let id = item['id'];
        let display_name = item['username']
        if (id != user) {
            let user_id = "#" + id;
            $("#user_details").clone().removeClass('d-none').appendTo("ui.contacts").attr("id", id);
            $("#" + id).find(".user_info").find(".user_name").html(display_name);
            // $(user_ids).on('click', function (event){
            //     body_children = $(".msg_card_body").children();
            //     body_len = body_children.length;
            //     for (var i = 0; i < body_len; i++){
            //         if ($(body_children[i]).attr("class") !== 'd-none'){
            //             $(body_children[i]).remove();
            //         }
            //     }
            //
            //     let element = event.currentTarget;
            //     let client = $(element).attr("id");
            //     let new_msg_url = msg_url + "?userid=" + client;
            //
            //     $('#sender_user_id').val(client);
            // });
            return users;
        }
    })
}