function demo_async_call() {
    let original_text = $("textarea[name='text']");
    let prompt = $("textarea[name='prompt']");
    let csrf = $("input[name='csrfmiddlewaretoken']");
    let result_text = $("textarea[name='result_text']");
    let temperature = document.querySelector("input[name='temperature']");
    let question = $("textarea[name='question']");
    let character = $("select[name='character']");

    if (original_text.val() == '' && question.val()=='') {
        return;
    }

    result_text.val('');
    result_text.hide();
    $("div[name='spinner']").show();

    const request_data = new FormData();
    request_data.append('original_text', original_text.val());
    request_data.append('prompt', prompt.val());
    request_data.append('temperature', temperature.value);
    request_data.append('csrfmiddlewaretoken', csrf.val());
    request_data.append('question', question.val());
    request_data.append('character', character.val());
    fetch("/demo_pdf_async/", {
        method: "POST",
        body: request_data,
    }).then(response => response.json()).then((response) => {
        result_text.val(response.result);
        $("div[name='spinner']").hide();
        result_text.show();
    });
}

function demo_init() {
    let timer;
    // $("textarea[name='text']").keyup(function () {
    //     clearTimeout(timer);
    //     timer = setTimeout(() => { demo_async_call(); }, 800);
    // });
    // $("textarea[name='prompt']").keyup(function () {
    //     clearTimeout(timer);
    //     timer = setTimeout(() => { demo_async_call(); }, 800);
    // });
    // $("input[name='temperature']").change(function () {
    //     clearTimeout(timer);
    //     timer = setTimeout(() => { demo_async_call(); }, 800);
    // });
    // $("textarea[name='question']").keyup(function () {
    //     clearTimeout(timer);
    //     timer = setTimeout(() => { demo_async_call(); }, 800);
    // });
    $('.send-button').click(function () {
        demo_async_call();
    });
}

$(document).ready(function () {
    demo_init();
})