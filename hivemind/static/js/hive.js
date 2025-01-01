function sortList(ul) {
    var ul = document.getElementById(ul);

    Array.from(ul.getElementsByTagName("li"))
        .sort((a, b) => a.textContent.localeCompare(b.textContent))
        .forEach(li => ul.appendChild(li));
}

$(document).ready(function () {
    var socket = io('/hive');
    var data = $('#data').data();
    const chatroom_id = data.chatroom_id
    const name = data.name
    const avatar = data.avatar
    console.log(avatar)
    var clone_msg = ''
    const snd_msg_template = document.getElementById('snd-message-template')
    const rcv_msg_template = document.getElementById('rcv-message-template')
    const user_list = document.getElementById('user_list')
    const user_sidebar_template = document.getElementById('user-sidebar-template')
    socket.on('connect', function () {
        socket.emit('join', {
            room: chatroom_id
        });
    });
    socket.on('add_to_userlist', function (data) {
        var new_user = data.new_user
        var user_sidebar = user_sidebar_template.content.cloneNode(true)
        user_sidebar.querySelector("#user_sidebar_name").textContent = new_user.name
        user_sidebar.querySelector("#sidebar-avatar").src = data.avatar
        user_sidebar.querySelector("li").setAttribute("data-user_id", new_user.id);
        user_list.appendChild(user_sidebar)
        sortList("user_list")
    });
    socket.on('remove_from_userlist', function (data) {
        var user_to_delete = data.user_to_delete
        var items = user_list.getElementsByTagName("li");
        for (var i = 0; i < items.length; ++i) {
            var data = parseInt(items[i].getAttribute('data-user_id'))
            if (data == user_to_delete) {
                user_list.removeChild(items[i])
                break
            }
        }
    });
    socket.on('status', function (data) {
        var div = document.createElement("div");
        div.textContent = data.msg
        div.classList.add("chat")
        div.classList.add("chat-end")
        $('#chat-message-container').append(div)
        $('#chat-message-container').scrollTop($('#chat-message-container')[0].scrollHeight);
    });
    socket.on('message', function (data) {
        if (data.user_id == '{{ current_user.id }}') {
            clone_msg = snd_msg_template.content.cloneNode(true)
        }
        else {
            clone_msg = rcv_msg_template.content.cloneNode(true)
        }
        var msg_avatar = clone_msg.getElementById('chat-avatar')
        var msg_header = clone_msg.getElementById('chat-header')
        var msg_content = clone_msg.getElementById('chat-content')
        msg_header.textContent = data.name
        msg_content.textContent = data.content
        msg_avatar.src = data.avatar
        $('#chat-message-container').append(clone_msg)
        $('#chat-message-container').scrollTop($('#chat-message-container')[0].scrollHeight);
    });
    $('#text').keypress(function (e) {
        const code = e.keyCode || e.which;
        if (code == 13) {
            text = $('#text').val();
            $('#text').val('');
            if (!(typeof text === "string" && text.length === 0)) {
                socket.emit('send_message', {
                    user_id: '{{ current_user.id }}',
                    name: name,
                    avatar: avatar,
                    content: text
                });
            }
        }
    });
    $("#send").click(function () {
        text = $('#text').val();
        $('#text').val('');
        if (!(typeof text === "string" && text.length === 0)) {
            socket.emit('send_message', {
                user_id: '{{ current_user.id }}',
                name: name,
                avatar: avatar,
                content: text
            });
        }
    });
});
