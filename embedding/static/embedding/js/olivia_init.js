function olivia_overall_init() {
    element_init();
    add_event_listener();
}

function element_init() {
    d0 = document.querySelector("div[name='entrance_0']");
    d1 = document.querySelector("div[name='entrance_1']");
    d2 = document.querySelector("div[name='entrance_2']");
    d3 = document.querySelector("div[name='entrance_3']");
    d4 = document.querySelector("div[name='entrance_4']");
    d5 = document.querySelector("div[name='entrance_5']");
    d6 = document.querySelector("div[name='entrance_6']");
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

    let buttons_1 = document.querySelectorAll("label[name='gender']");
    buttons_1.forEach(e => {
        e.addEventListener("click", function (e) {
            next_entrance();
        });
    });

    let buttons_2 = document.querySelector("div[name='old_user']");
    buttons_2.addEventListener("click", function (e) {
        hide(d0);
        flow_messages(5);
        flow_finish();
    });

    let buttons_3 = document.querySelector("div[name='new_user']");
    buttons_3.addEventListener("click", function (e) {
        hide(d0);
        localStorage.setItem('olivia_username', '');
        flow_messages(1);
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