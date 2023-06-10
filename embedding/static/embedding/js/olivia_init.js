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

    let buttons_gender = document.querySelectorAll("label[name='gender']");
    buttons_gender.forEach(e => {
        e.addEventListener("click", function (e) {
            next_entrance();
        });
    });

    let buttons_age = document.querySelectorAll("label[name='age']");
    buttons_age.forEach(e => {
        e.addEventListener("click", function (e) {
            next_entrance();
        });
    });

    let buttons_old_user = document.querySelector("div[name='old_user']");
    buttons_old_user.addEventListener("click", function (e) {
        hide(d0);
        flow_messages(5);
        flow_finish();
    });

    let buttons_new_user = document.querySelector("div[name='new_user']");
    buttons_new_user.addEventListener("click", function (e) {
        hide(d0);
        localStorage.removeItem("olivia_username");
        localStorage.removeItem("olivia_d_uuid");
        localStorage.removeItem("olivia_uuid");
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