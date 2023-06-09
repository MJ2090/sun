let controller = new AbortController();

$(document).ready(function () {
    olivia_overall_init();
    flow_messages(1);
})

function flow_messages(page_number) {
    let messages = document.querySelectorAll("[name='msg_" + page_number + "']")
    let parent = document.querySelector("div[name='entrance_" + page_number + "']")
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
    let d1 = document.querySelector("div[name='entrance_1']");
    let d2 = document.querySelector("div[name='entrance_2']");
    let d3 = document.querySelector("div[name='entrance_3']");
    let d4 = document.querySelector("div[name='entrance_4']");
    let d5 = document.querySelector("div[name='entrance_5']");
    if (isShown(d1)) {
        hide(d1);
        show(d2);
        flow_messages(2);
    } else if (isShown(d2)) {
        hide(d2);
        show(d3);
        flow_messages(3);
    } else if (isShown(d3)) {
        hide(d3);
        show(d4);
        flow_messages(4);
    } else {
        hide(d4);
        show(d5);
        flow_messages(5);
        entrance_finish();
    }
}

function entrance_finish() {
   setTimeout(olivia_chat_init, TRANSITION_INTERVAL);
}