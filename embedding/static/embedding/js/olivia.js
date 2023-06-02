const BASE_INTERVAL = 500

function chat_async_call() {
}

function flow_messages(messages) {
    let index = 0;
    let t = setInterval(show_messages, BASE_INTERVAL);

    function show_messages() {
        fadeIn(messages[index]);
        index += 1;
        if (index == messages.length) {
            clearInterval(t);
            let textarea = document.querySelector("textarea");
            textarea.focus();
            textarea.click();
        }
    }
}

function fadeIn(element) {
    element.classList.add('fade-in');
}

function fadeOut(element) {
    element.classList.add('fade-out');
}

function olivia_init() {
    add_event_listener();
    flow_messages(document.querySelectorAll("[name='msg_1']"));
}

function add_event_listener() {
    let textarea = document.querySelector("textarea");
    textarea.addEventListener("keydown", function (e) {
        if (e.key === 'Enter') {
            next_entrance();
            return false;
        }
    });
}

function next_entrance() {
    d1 = document.querySelector("div[name='entrance_1']");
    fadeOut(d1);
    d2 = document.querySelector("div[name='entrance_2']");
    fadeIn(d2);
}

$(document).ready(function () {
    olivia_init();
})
