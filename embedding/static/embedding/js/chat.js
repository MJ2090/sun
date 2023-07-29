let timer;
let controller = new AbortController();

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
        if (old_msg.get(i).getAttribute('name') == 'ai_msg') {
            role = 'assistant'
        } else {
            role = 'user'
        }
        let dic = { "role": role, "content": old_msg.get(i).innerText }
        history_msg.push(dic);
    }
    let history = JSON.stringify(history_msg);
    character.prop("disabled", true);
    model_selector.prop("disabled", true);
    let new_msg_text = new_msg.val();
    new_msg.val('');

    let content = $('.message-container');

    let human_title = $("div[name='human_title']").clone();
    content.append(human_title.get(0));

    let human_msg = document.querySelector("div[name='human_msg']").cloneNode(true);
    let human_msg_child = human_msg.children[0];
    human_msg_child.classList.add("dialogue");
    human_msg_child.innerText = new_msg_text;
    content.append(human_msg);

    $("div[name='spinner']").show();
    timer = setTimeout(() => { display_still_thinking(); }, 10000);
    $(".message-outer-container").animate({ scrollTop: $(".message-container").height() }, "fast");

    // abort previous call if any
    controller.abort();
    controller = new AbortController();

    const request_data = new FormData();
    request_data.append('message', new_msg_text);
    request_data.append('character', character.val());
    request_data.append('history', history);
    request_data.append('model', model.val());
    request_data.append('enable_speech', enable_speech[0].checked);
    request_data.append('dialogue_id', $("input[name='dialogue_id']").val());
    request_data.append('csrfmiddlewaretoken', csrf.val());
    fetch("/chat_async/", {
        method: "POST",
        body: request_data,
        signal: controller.signal,
    })
        .then(
            response => response.json())
        .then((response) => {
            let ai_title = $("div[name='ai_title']").clone();
            content.append(ai_title.get(0));

            let ai_message = response.ai_message;
            let is_code = ai_message.indexOf('```') != -1;
            while (true) {
                my_ind = ai_message.indexOf('```');
                if (my_ind == -1) {
                    break;
                }

                ai_message = ai_message.replace(/\n*```\n*/, '<pre><code>');
                ai_message = ai_message.replace(/\n*```\n*/, '</pre></code>');
            }

            pre_process();
            display_msg(ai_message, is_code);
            post_process();

            audio_process(response.audio_address, enable_speech[0].checked);
        });
}

function display_msg(ai_message, is_code) {
    msg_len = ai_message.length;
    final_list = [];
    current_message = '';
    message_list = ai_message.split('\n\n');
    single_section_limit = 400;
    if (is_code) {
        single_section_limit = 100000;
    }
    for (let i = 0; i < message_list.length; i++) {
        if (current_message != '') {
            current_message += '\n\n';
        }
        current_message += message_list[i];
        if (current_message.length > single_section_limit || i == message_list.length - 1) {
            final_list.push(current_message);
            current_message = '';
        }
    }

    display_msg_piece(final_list, 0);
}

function display_msg_piece(final_list, current_index) {
    let content = $('.message-container');
    if (current_index > 0) {
        let ai_title = $("div[name='ai_title']").clone();
        content.append(ai_title.get(0));
    }
    let ai_msg = document.querySelector("div[name='ai_msg']").cloneNode(true);
    let ai_msg_child = ai_msg.children[0];
    ai_msg_child.classList.add("dialogue");
    ai_msg_child.innerHTML = final_list[current_index];
    content.append(ai_msg);
    hljs.highlightAll();
    if (current_index == 0) {
        $(".message-outer-container").animate({ scrollTop: $(".message-container").height() }, 400);
    }

    if (current_index >= final_list.length - 1) {
        post_process();
    } else {
        setTimeout(() => { display_msg_piece(final_list, current_index + 1); }, 3000);
    }
}

function audio_process(audio_address, enabled) {
    if (enabled && audio_address != '') {
        let source = $("source[name='source']");
        source.attr('src', '/static/embedding/media/' + audio_address + '.mp3');
        let audio = $("audio[name='audio']");
        audio[0].load();
    }
}

function pre_process() {
    $("div[name='spinner']").hide();
    $(".still-thinking").hide();
    clearTimeout(timer);
}

function post_process() {
    let new_msg = $("input[name='message']");
    new_msg.focus();
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
