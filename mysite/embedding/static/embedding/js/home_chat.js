function async_call() {
    let new_msg = $("input[name='message']");
    if (new_msg.val() == "") {
        return;
    }
    let csrf = $("input[name='csrfmiddlewaretoken']");
    let old_msg = $(".dialogue");
    let history_msg = [];
    let role = "user";
    for (let i = 0; i < old_msg.length; i++) {
        let dic = { "role": role, "content": old_msg.get(i).innerText }
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

    $.ajax({
        type: 'POST',
        url: "/sendchat_home/",
        data: {
            message: new_msg_text,
            history: history,
            csrfmiddlewaretoken: csrf.val(),
        },
        success: function (response) {
            let data = JSON.parse(response);
            let ai_message = data.ai_message
            new_msg.prop("disabled", false);
            new_msg.focus();
            let content = $('.message-container');

            $("div[name='spinner").hide();
            let ai_msg = $("p[name='ai_msg']").clone();
            ai_msg.text(ai_message);
            ai_msg.addClass("dialogue");
            content.append(ai_msg.get(0));
            $(".message-inner-container").animate({ scrollTop: $(".message-container").height() }, "fast");
        },
    })
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
        async_call();
    });

    $("input[name='message']").keydown(function (e) {
        if (e.keyCode == 13) {
            async_call();
            return false;
        }
    });
}

$(document).ready(function () {
    home_chat_init();
})