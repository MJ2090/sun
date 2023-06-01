let timer;

function chat_async_call() {
}


function olivia_init() {
    let textarea = document.querySelector("textarea");
    textarea.focus();
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
