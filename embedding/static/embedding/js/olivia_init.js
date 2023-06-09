function olivia_overall_init() {
    add_event_listener();
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
            next_entrance();
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