let controller = new AbortController();

let d1 = document.querySelector("div[name='entrance_1']");
let d2 = document.querySelector("div[name='entrance_2']");
let d3 = document.querySelector("div[name='entrance_3']");
let d4 = document.querySelector("div[name='entrance_4']");
let d5 = document.querySelector("div[name='entrance_5']");
let d6 = document.querySelector("div[name='entrance_6']");

$(document).ready(function () {
    olivia_overall_init();
    if (localStorage.olivia_username) {
        document.querySelector("span[name='first_page_username']").innerHTML = localStorage.olivia_username;
        flow_messages(6);
    } else {
        flow_messages(1);
    }
})

function flow_messages(page_number) {
    let messages = document.querySelectorAll("[name='msg_" + page_number + "']")
    let parent = document.querySelector("div[name='entrance_" + page_number + "']")
    show(parent);
    let index = 0;
    let t = setInterval(show_messages, BASE_INTERVAL);

    function show_messages() {
        fadeIn(messages[index]);
        index += 1;
        if (index == messages.length) {
            clearInterval(t);
            let maybe_input = parent.querySelector("input[type='text']");
            if (maybe_input) {
                maybe_input.focus();
                maybe_input.click();
            }
        }
    }
}

function next_entrance() {
    if (isShown(d1)) {
        hide(d1);
        flow_messages(2);
    } else if (isShown(d2)) {
        hide(d2);
        flow_messages(3);
    } else if (isShown(d3)) {
        hide(d3);
        flow_messages(4);
    } else {
        hide(d4);
        flow_messages(5);
        flow_finish();
    }
}

function flow_finish() {
   setTimeout(olivia_chat_init, TRANSITION_INTERVAL);
}