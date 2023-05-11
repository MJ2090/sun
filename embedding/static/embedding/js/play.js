function play_fetch() {
    let original_iamge = document.querySelector("input[name='image_f']");
    let csrf = document.querySelector("input[name='csrfmiddlewaretoken']");

    const request_data = new FormData();
    request_data.append('original_iamge', original_iamge.files[0]);
    request_data.append('csrfmiddlewaretoken', csrf.value);
    fetch("/play_async/", {
        method: "POST",
        body: request_data,
    }).then(response => response.json()).then((response) => {
        let data = response;
        question = document.querySelector("textarea[name='response_question']")
        answer = document.querySelector("textarea[name='response_answer']")
        question.value = data.question;
        answer.value = data.question;
        question;
    });
}

function play_init() {
    // $(".send-button")
    document.querySelector(".send-button").addEventListener('click', function () {
        play_fetch();
    });
}

$(document).ready(function () {
    play_init();
})