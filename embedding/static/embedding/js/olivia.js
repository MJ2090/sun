function chat_async_call() {
}

function flow_messages() {
    messages = document.querySelectorAll("[name='msg_1']");
    let base_interval = 2000;
    let index = 0;
    let t = setInterval(show_messages, base_interval);

    function show_messages() {
        fadeIn(messages[index]);
        if (index == messages.length-1) {
            clearInterval(t);
            messages[index].focus();
            messages[index].click();
        }
        index += 1;
    }
}

function fadeIn(element) {
    // ensure the element is initially hidden
    element.classList.add('fade-in');
}

function removeClass(el) {
    el.classList.remove('opacity_zero');
}

function olivia_init() {
    add_event_listener();
    flow_messages();
}

function add_event_listener() {
    let textarea = document.querySelector("textarea");
    textarea.addEventListener("keydown", function (e) {
        if (e.keyCode == 13) {
            chat_async_call();
            return false;
        }
    });
}

$(document).ready(function () {
    olivia_init();
})
