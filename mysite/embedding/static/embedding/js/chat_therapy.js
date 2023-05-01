let timer;

function chat_async_call() {
    let new_msg = $("input[name='message']");
    let button = $("button[name='send_button']");
    if (new_msg.val() == "" || button.prop("disabled")) {
        return;
    }
    let csrf = $("input[name='csrfmiddlewaretoken']");
    let enable_speech = $("input[name='enable_speech']");
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
    button.prop("disabled", true);
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
    timer = setTimeout(() => { display_still_thinking(); }, 5000);
    $(".message-outer-container").animate({ scrollTop: $(".message-container").height() }, "fast");

    const request_data = new FormData();
    request_data.append('message', new_msg_text);
    request_data.append('history', history);
    request_data.append('enable_speech', enable_speech[0].checked);
    request_data.append('dialogue_id', $("input[name='dialogue_id']").val());
    request_data.append('csrfmiddlewaretoken', csrf.val());
    fetch("/sendchat_therapy_async/", {
        method: "POST",
        body: request_data,
    })
    .then(
        response => response.json())
    .then((response) => {
        let data = response;
        let ai_message = data.ai_message;
        while (true) {
            my_ind = ai_message.indexOf('```');
            if (my_ind == -1) {
                break;
            }

            ai_message = ai_message.replace(/\n*```\n*/, '<pre><code>');
            ai_message = ai_message.replace(/\n*```\n*/, '</pre></code>');
        }
        let audio_address = data.audio_address;
        button.prop("disabled", false);
        new_msg.focus();
        let content = $('.message-container');

        $("div[name='spinner").hide();
        $(".still-thinking").hide();
        clearTimeout(timer);
        let ai_msg = $("p[name='ai_msg']").clone();
        ai_msg.get(0).innerHTML = ai_message
        ai_msg.addClass("dialogue");
        content.append(ai_msg.get(0));
        hljs.highlightAll();
        $(".message-outer-container").animate({ scrollTop: $(".message-container").height() }, "fast");

        if (enable_speech[0].checked && audio_address != '') {
            let source = $("source[name='source']");
            source.attr('src', '/static/embedding/media/' + audio_address + '.mp3');
            let audio = $("audio[name='audio']");
            audio[0].load();
        }
    });
}

function display_still_thinking() {
    const words = ["still thinking ..", "one moment ..", "needs more time ..", "thanks for waiting ..",];
    const w_indix = Math.floor(Math.random() * words.length);
    $('.still-thinking').text(words[w_indix]);
    $('.still-thinking').show();
}

function chat_init() {
    $('.send-button').click(function () {
        chat_async_call();
    });

    $("input[name='message']").keydown(function (e) {
        if (e.keyCode == 13) {
            chat_async_call();
            return false;
        }
    });

    // Audio play starts
    $("input[name='enable_speech']").click(function () {
        if (!this.checked) {
            let audio = $("audio[name='audio']");
            audio[0].pause();
        }
        $("audio[name='audio']").toggle(this.checked);
    });

    $("audio[name='audio']").on('canplaythrough', function () {
        this.play();
    });
    // Audio play ends
}

$(document).ready(function () {
    chat_init();
})