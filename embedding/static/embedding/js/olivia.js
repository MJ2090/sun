const BASE_INTERVAL = 100
let t_name = ''
let t_age = ''
let t_gender = ''

function chat_async_call() {
}

function flow_messages(messages, callback) {
    let index = 0;
    let t = setInterval(show_messages, BASE_INTERVAL);

    function show_messages() {
        fadeIn(messages[index]);
        index += 1;
        if (index == messages.length) {
            clearInterval(t);
            if (callback != null) {
                callback();
            }
        }
    }
}

function setFocus() {
    let textarea = document.querySelector("textarea");
    textarea.focus();
    textarea.click();
}

function fadeIn(element) {
    element.classList.add('fade-in');
}

function fadeOut(element) {
    element.classList.add('fade-out');
}

function olivia_init() {
    add_event_listener();
    flow_messages(document.querySelectorAll("[name='msg_1']"), setFocus);
}

function add_event_listener() {
    let textareas = document.querySelectorAll("textarea");
    textareas.forEach(e => {
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

}

function entrance_finish() {
    let d3 = document.querySelector("div[name='entrance_3']");
    d3.remove();
    flow_messages(document.querySelectorAll("[name='msg_4']"), null);
    therapy_init();
}

function therapy_init() {
    const request_data = new FormData();
    request_data.append('t_name', t_name);
    request_data.append('t_age', t_age);
    request_data.append('t_gender', t_gender);
    request_data.append('csrfmiddlewaretoken', csrf.val());
    fetch("/therapy_init/", {
        method: "POST",
        body: request_data,
    })
    .then(
        response => response.json())
    .then((response) => {
        console.log(response);
    });
}

function next_entrance() {
    let d1 = document.querySelector("div[name='entrance_1']");
    let d2 = document.querySelector("div[name='entrance_2']");
    if (d1 != null) {
        d1.remove();
        flow_messages(document.querySelectorAll("[name='msg_2']"), setFocus);
    } else {
        d2.remove();
        flow_messages(document.querySelectorAll("[name='msg_3']"), null);
    }
}

$(document).ready(function () {
    olivia_init();
})
