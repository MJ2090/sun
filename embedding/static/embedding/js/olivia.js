const BASE_INTERVAL = 100

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
    let t_name = document.querySelector("textarea[name='msg_1']");
    flow_messages(document.querySelectorAll("[name='msg_1']"), setFocus, t_name);
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
    let d4 = document.querySelector("div[name='entrance_4']");
    hide(d3);
    show(d4);
    flow_messages(document.querySelectorAll("[name='msg_4']"), null);
    therapy_init();
}

function therapy_init() {
    let csrf = $("input[name='csrfmiddlewaretoken']");
    const request_data = new FormData();
    t_name = document.querySelector("textarea[name='msg_1']").value;
    t_age = document.querySelector("textarea[name='msg_2']").value;
    t_gender = 'Female';
    request_data.append('t_name', t_name);
    request_data.append('t_age', t_age);
    request_data.append('t_gender', t_gender);
    request_data.append('csrfmiddlewaretoken', csrf.val());
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
    });
}

function next_entrance() {
    let d1 = document.querySelector("div[name='entrance_1']");
    let d2 = document.querySelector("div[name='entrance_2']");
    let d3 = document.querySelector("div[name='entrance_3']");
    if (isShown(d1)) {
        hide(d1);
        show(d2);
        let t_age = document.querySelector("textarea[name='msg_2']");
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
