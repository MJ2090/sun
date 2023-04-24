function chat_async_call() {
    let new_msg = $("input[name='message']");
    if (new_msg.val() == "") {
        return;
    }
    let character = $("select[name='character']");
    let model = $("select[name='training_model']");
    let csrf = $("input[name='csrfmiddlewaretoken']");
    let model_selector = $("select[name='training_model']");
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
    new_msg.prop("disabled", true);
    character.prop("disabled", true);
    model_selector.prop("disabled", true);
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
    $(".message-outer-container").animate({ scrollTop: $(".message-container").height() }, "fast");

    const request_data = new FormData();
    request_data.append('message', new_msg_text);
    request_data.append('character', character.val());
    request_data.append('history', history);
    request_data.append('model', model.val());
    request_data.append('enable_speech', enable_speech[0].checked);
    request_data.append('dialogue_id', $("input[name='dialogue_id']").val());
    request_data.append('csrfmiddlewaretoken', csrf.val());
    fetch("/sendchat/", {
        method: "POST",
        body: request_data,
    })
    .then(
        response => response.json())
    .then((response) => {
        let data = response;
        let ai_message = data.ai_message.replace(/(?:\r\n|\r|\n)/g, "<br>");
        let audio_address = data.audio_address;
        new_msg.prop("disabled", false);
        new_msg.focus();
        let content = $('.message-container');

        $("div[name='spinner").hide();
        let ai_msg = $("p[name='ai_msg']").clone();
        ai_msg.get(0).innerHTML = ai_message
        ai_msg.addClass("dialogue");
        content.append(ai_msg.get(0));
        $(".message-outer-container").animate({ scrollTop: $(".message-container").height() }, "fast");

        if (enable_speech[0].checked && audio_address != '') {
            let source = $("source[name='source']");
            source.attr('src', '/static/embedding/media/' + audio_address + '.mp3');
            let audio = $("audio[name='audio']");
            audio[0].load();
        }
    });
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