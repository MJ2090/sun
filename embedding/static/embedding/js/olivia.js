const BASE_INTERVAL = 150
const TRANSITION_INTERVAL = 400
let controller = new AbortController();

function flow_messages(messages, callback, el) {
    let index = 0;
    let t = setInterval(show_messages, BASE_INTERVAL);

    function show_messages() {
        fadeIn(messages[index]);
        index += 1;
        if (index == messages.length) {
            clearInterval(t);
            if (callback != null) {
                callback(el);
            }
        }
    }
}

function setFocus(el) {
    el.focus();
    el.click();
}

function fadeIn(element) {
    element.classList.add('fade-in');
}

function fadeOut(element) {
    element.classList.add('fade-out');
}

function hide(element) {
    element.classList.add('hidden');
}

function show(element) {
    element.classList.remove('hidden');
}

function isShown(element) {
    return !element.classList.contains('hidden');
}

function olivia_init() {
    add_event_listener();
    let t_name = document.querySelector("input[name='msg_1']");
    flow_messages(document.querySelectorAll("[name='msg_1']"), setFocus, t_name);
}

function add_event_listener() {
    let inputs = document.querySelectorAll("input[type='text']");
    inputs.forEach(e => {
        e.addEventListener("keydown", function (e) {
            if (e.key === 'Enter') {
                next_entrance();
                return false;
            }
        });
    })

    let buttons = document.querySelectorAll("label[name='gender']");
    buttons.forEach(e => {
        e.addEventListener("click", function (e) {
            entrance_finish();
        });
    });

    let textarea = document.querySelector("textarea");
    textarea.addEventListener("keypress", function (e) {
        if (e.key === 'Enter') {
            therapy_chat();
            e.preventDefault();
            return false;
        }
    });
}

function entrance_finish() {
    let d3 = document.querySelector("div[name='entrance_3']");
    let d4 = document.querySelector("div[name='entrance_4']");
    hide(d3);
    show(d4);
    flow_messages(document.querySelectorAll("[name='msg_4']"), null);
    setTimeout(therapy_init, TRANSITION_INTERVAL);
}

function get_history_messages() {
    let history_elements = $(".dialogue");
    let history_msg_dic = [];
    let role = "user";
    for (let i = 0; i < history_elements.length; i++) {
        if (history_elements.get(i).getAttribute('name') == 'ai_msg') {
            role = 'assistant'
        } else {
            role = 'user'
        }
        let dic = { "role": role, "content": history_elements.get(i).innerText }
        history_msg_dic.push(dic);
    }
    let history_str = JSON.stringify(history_msg_dic)
    return history_str;
}

function scroll_up() {
    $(".message-outer-container").animate({ scrollTop: $(".message-container").height() }, "fast");
}

function toggle_spinner(show) {
    if (show) {
        document.querySelector("div[name='spinner").classList.remove("invisible");
    } else {
        document.querySelector("div[name='spinner").classList.add("invisible");
    }
}

function therapy_chat() {
    // prepare data
    let csrf = document.querySelector("input[name='csrfmiddlewaretoken']").value;
    let history_str = get_history_messages();
    let new_msg_text = document.querySelector("textarea").value;
    let uuid = document.querySelector("div[name='uuid']").value;
    const request_data = new FormData();
    request_data.append('history', history_str);
    request_data.append('message', new_msg_text);
    request_data.append('uuid', uuid);
    request_data.append('csrfmiddlewaretoken', csrf);

    // prepare UI
    let content = $('.message-container');
    let human_msg = $("p[name='human_msg']").clone();
    human_msg.addClass("dialogue");
    human_msg.text(new_msg_text);
    content.append(human_msg.get(0));
    document.querySelector("textarea").value = '';
    toggle_spinner(true);
    scroll_up();

    // abort previous call if any
    controller.abort();
    controller = new AbortController();
    // api fetch
    fetch("/olivia_async_chat/", {
        method: "POST",
        body: request_data,
        signal: controller.signal,
    })
        .then(
            response => response.json())
        .then((response) => {
            pre_process();
            display_msg(response.ai_message);
            post_process();
        })
        .catch((e) => {
            console.log(777888);
        });
}

function therapy_init() {
    // prepare data
    let csrf = $("input[name='csrfmiddlewaretoken']");
    t_name = document.querySelector("input[name='msg_1']").value;
    t_age = document.querySelector("input[name='msg_2']").value;
    t_gender = 'Female';
    const request_data = new FormData();
    request_data.append('t_name', t_name);
    request_data.append('t_age', t_age);
    request_data.append('t_gender', t_gender);
    request_data.append('csrfmiddlewaretoken', csrf.val());

    // api fetch
    fetch("/olivia_async_init/", {
        method: "POST",
        body: request_data,
    })
        .then(
            response => response.json())
        .then((response) => {
            let d4 = document.querySelector("div[name='entrance_4']");
            let d5 = document.querySelector("div[name='entrance_5']");
            hide(d4);
            show(d5);
            console.log(response);
            display_msg(response.ai_message);
            let uuid = document.querySelector("div[name='uuid']");
            uuid.value = response.uuid;
        });
}

function next_entrance() {
    let d1 = document.querySelector("div[name='entrance_1']");
    let d2 = document.querySelector("div[name='entrance_2']");
    let d3 = document.querySelector("div[name='entrance_3']");
    if (isShown(d1)) {
        hide(d1);
        show(d2);
        let t_age = document.querySelector("input[name='msg_2']");
        flow_messages(document.querySelectorAll("[name='msg_2']"), setFocus, t_age);
    } else {
        hide(d2);
        show(d3);
        flow_messages(document.querySelectorAll("[name='msg_3']"), null, null);
    }
}

$(document).ready(function () {
    olivia_init();
})

function display_msg(ai_message) {
    message_list = ai_message.split('\n\n');
    display_msg_piece(message_list, 0);
}

function display_msg_piece(final_list, current_index) {
    let content = $('.message-container');
    let ai_msg = $("p[name='ai_msg']").clone();
    ai_msg.css('display', 'none');
    ai_msg.get(0).innerHTML = final_list[current_index];
    ai_msg.addClass("dialogue");
    content.append(ai_msg.get(0));
    ai_msg.fadeIn();
    if (current_index == 0) {
        scroll_up();
    }

    if (current_index >= final_list.length - 1) {
        post_process();
    } else {
        setTimeout(() => { display_msg_piece(final_list, current_index + 1); }, 3000);
    }
}

function pre_process() {
    toggle_spinner(false);
    $(".still-thinking").hide();
}

function post_process() {
    let new_msg = $("input[name='message']");
    let button = $("button[name='send_button']");
    button.prop("disabled", false);
    new_msg.focus();
}
