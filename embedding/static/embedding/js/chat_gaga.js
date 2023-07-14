function chat_async_call() {
    let new_msg = $("input[name='message']");
    let button = $("button[name='send_button']");
    if (new_msg.val() == "" || button.prop("disabled")) {
        return;
    }
    let csrf = $("input[name='csrfmiddlewaretoken']");
    const character = document.querySelector("select[name='character']");
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

    $("div[name='spinner']").show();
    $(".message-outer-container").animate({ scrollTop: $(".message-container").height() }, "fast");

    let source_id = $("input[name='source_id']").val();

    const request_data = new FormData();
    request_data.append('message', new_msg_text);
    request_data.append('history', history);
    request_data.append('dialogue_id', $("input[name='dialogue_id']").val());
    request_data.append('csrfmiddlewaretoken', csrf.val());
    request_data.append('source_id', source_id);
    request_data.append('character', character.value);
    fetch("/chat_async_gaga/", {
        method: "POST",
        body: request_data,
    })
    .then(
        response => response.json())
    .then((response) => {
        const rewritten_query = document.querySelector("input[name='rewritten_query']");
        rewritten_query.value = response.rewritten_query;
        let ai_message = response.ai_message;
        while (true) {
            my_ind = ai_message.indexOf('```');
            if (my_ind == -1) {
                break;
            }

            ai_message = ai_message.replace(/\n*```\n*/, '<pre><code>');
            ai_message = ai_message.replace(/\n*```\n*/, '</pre></code>');
        }

        pre_process();
        display_msg(ai_message);
        post_process();
    });
}

function display_msg(ai_message) {
    final_list = ai_message.split('\n\n');
    display_msg_piece(final_list, 0);
}

function display_msg_piece(final_list, current_index) {
    let content = $('.message-container');
    if (current_index > 0) {
        let ai_title = $("div[name='ai_title']").clone();
        content.append(ai_title.get(0));
    }
    let ai_msg = $("p[name='ai_msg']").clone();
    ai_msg.css('display', 'none');
    ai_msg.get(0).innerHTML = final_list[current_index];
    ai_msg.addClass("dialogue");
    content.append(ai_msg.get(0));
    ai_msg.fadeIn();
    hljs.highlightAll();
    if (current_index==0) {
        $(".message-outer-container").animate({ scrollTop: $(".message-container").height() }, 400);
    }

    if (current_index >= final_list.length - 1) {
        post_process();
    } else {
        setTimeout(() => { display_msg_piece(final_list, current_index + 1); }, 3000);
    }
}

function pre_process() {
    $("div[name='spinner']").hide();
    $(".still-thinking").hide();
}

function post_process() {
    let new_msg = $("input[name='message']");
    let button = $("button[name='send_button']");
    button.prop("disabled", false);
    new_msg.focus();
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

    setTimeout(() => {
        const words = ["Hello, how are you today?", "Hi, how's everything going?", "Hey, how are you?", "Hello, are you doing well today?",];
        const w_indix = Math.floor(Math.random() * words.length);
        $('.first-msg-2').text(words[w_indix]);
        $('.first-msg-1').fadeIn();
        $('.first-msg-2').fadeIn();
     }, 1000);
}

$(document).ready(function () {
    chat_init();
})
