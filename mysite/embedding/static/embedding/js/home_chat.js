async function home_chat_fetch() {
    let new_msg = $("input[name='message']");
    if (new_msg.val() == "") {
        return;
    }
    let csrf = $("input[name='csrfmiddlewaretoken']");
    let old_msgs = $(".dialogue");
    let history_msg = [];
    let role = "user";
    for (let i = 0; i < old_msgs.length; i++) {
        let dic = { "role": role, "content": old_msgs.get(i).innerText }
        history_msg.push(dic);
        if (role == "user") {
            role = "assistant";
        } else {
            role = "user";
        }
    }
    let history = JSON.stringify(history_msg)
    new_msg.prop("disabled", true);
    let new_msg_text = new_msg.val();
    new_msg.val('');

    let content = $('.message-container');

    let human_title = $("div[name='human_title']").clone();
    content.append(human_title.get(0));

    let human_msg = $("p[name='human_msg']").clone();
    human_msg.addClass("dialogue");
    human_msg.text(new_msg_text);
    content.append(human_msg.get(0));

    let ai_title = $("div[name='ai_title']").clone();
    content.append(ai_title.get(0));

    $("div[name='spinner").show();
    $(".message-inner-container").animate({ scrollTop: $(".message-container").height() }, "fast");

    const request_data = new FormData();
    request_data.append('message', new_msg_text);
    request_data.append('history', history);
    request_data.append('csrfmiddlewaretoken', csrf.val());

    fetch("/sendchat_home/", {
      method: "POST",
      body: request_data,
    }).then(response => response.json()).then((response) => {
        let data = response;
        let ai_message = data.ai_message.replace(/(?:\r\n|\r|\n)/g, "<br>");
        let action_message = data.action_message
        let content = $('.message-container');

        new_msg.prop("disabled", false);
        new_msg.focus();

        $("div[name='spinner").hide();

        if (ai_message) {
            let ai_msg = $("p[name='ai_msg']").clone();
            ai_msg.get(0).innerHTML = ai_message
            ai_msg.addClass("dialogue");
            content.append(ai_msg.get(0));
        }

        let action = data.ai_action;
        if (action == '1') {
            ai_msg = $("p[name='ai_msg']").clone();
            ai_msg.text(action_message);
            content.append(ai_msg.get(0));

            let action_msg = $("a[name='ai_action']").clone();
            content.append(action_msg.get(0));
        }

        $(".message-inner-container").animate({ scrollTop: $(".message-container").height() }, "fast");
    },);
}

function open_chat() {
    $("div[name='home_chat_icon']").hide();
    $("div[name='home_chat_content']").fadeIn(300);
    $("input[name='message']").focus();
}

function close_chat() {
    $("div[name='home_chat_icon']").show();
    $("div[name='home_chat_content']").fadeOut(300);
}

function home_chat_init() {
    $("div[name='home_chat_icon']").click(function () {
        open_chat();
    });

    $("div[name='home_chat_close_icon']").click(function () {
        close_chat();
    });

    $('.send-button').click(function () {
        home_chat_fetch();
    });

    $("input[name='message']").keydown(function (e) {
        if (e.keyCode == 13) {
            home_chat_fetch();
            return false;
        }
    });
}

$(document).ready(function () {
    home_chat_init();
})